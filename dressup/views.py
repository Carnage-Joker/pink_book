from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop
from django.http import HttpRequest, HttpResponse


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    View to handle the creation of a new Avatar for the logged-in user.
    """
    if Avatar.objects.filter(user=request.user).exists():
        messages.error(
            request, "You already have an avatar. Redirecting to the mall.")
        return redirect('dressup:mall')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user
            avatar.save()

            # Equip the default starter outfit
            try:
                starter_items = [
                    "Barely Boyish",
                    "Tight Jeans",
                    "Tank Top",
                    "Sneakers",
                ]
                for item_name in starter_items:
                    item = Item.objects.get(name=item_name)
                    avatar.equip_item(item)

                avatar.save()
                messages.success(
                    request, "Your avatar has been created successfully and is wearing the default outfit!")

            except Item.DoesNotExist as e:
                messages.error(
                    request, f"An item from the starter outfit could not be equipped: {e}")

            return redirect('dressup:story_intro')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AvatarCreationForm()

    return render(request, 'dressup/create_avatar.html', {'form': form})


@login_required
@avatar_required
def story_intro_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the introduction to the story mode.
    """
    messages.success(request, "Your avatar is ready for the adventure!")
    return render(request, 'dressup/story_intro.html')

@login_required
@avatar_required
def mall_view(request):
    """
    Displays the mall where users can upgrade their avatars.
    """
    # Retrieve the user's avatar safely
    avatar = getattr(request.user, 'sissy_avatar', None)
    if avatar is None:
        messages.error(request, "You need to create an avatar first!")
        return redirect('dressup:create_avatar')

    # Fetch all shops and paginate them
    shops = Shop.objects.all().order_by('id')
    paginator = Paginator(shops, 10)  # 10 shops per page
    page_number = request.GET.get('page')
    shops_page = paginator.get_page(page_number)

    # Prepare image URLs for the avatar
    try:
        layer_keys = ['body', 'skirt', 'top', 'shoes', 'hair', 'accessories']
        image_urls = avatar.get_image_urls(layer_keys)
    except Exception as e:
        messages.error(
            request, "An error occurred while loading your avatar. Please try again.")
        image_urls = {}

    context = {
        'shops': shops_page,
        'avatar': avatar,
        'image_urls': image_urls,
        'layer_keys': layer_keys,
    }
    return render(request, 'dressup/mall.html', context)

@login_required
@avatar_required
def shop_detail(request, shop_id):
    """
    Displays details of a specific shop and handles item purchases.
    """
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(shop.items, id=item_id)
        avatar = request.user.avatar

        if PurchasedItem.objects.filter(user=request.user, item=item).exists():
            messages.info(request, "You have already purchased this item.")
        else:
            PurchasedItem.objects.create(user=request.user, item=item)
            messages.success(
                request, f"You have successfully purchased {item.name}!")
            return redirect('dressup:mall')

    return render(request, 'dressup/shop_detail.html', {'shop': shop, 'items': items})


@login_required
@avatar_required
def inventory_view(request):
    """
    Displays the user's purchased items and their equip status.
    """
    avatar = getattr(request.user, 'sissy_avatar', None)
    if not avatar:
        messages.error(request, "You need to create an avatar first!")
        return redirect('dressup:create_avatar')

    # Retrieve purchased and equipped items
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    equipped_items = avatar.equipped_items.all() if avatar else []

    if request.method == 'POST' or request.GET.get('item_id'):
        item_id = request.POST.get('item_id') or request.GET.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        # Toggle equip/unequip status
        if item in equipped_items:
            avatar.unequip_item(item)
            messages.success(request, f"{item.name} has been unequipped.")
        else:
            avatar.equip_item(item)
            messages.success(request, f"{item.name} has been equipped.")

        # Refresh equipped items after changes
        equipped_items = avatar.equipped_items.all()

    context = {
        'purchased_items': purchased_items,
        'equipped_items': equipped_items,
    }
    return render(request, 'dressup/inventory.html', context)


@login_required
@avatar_required
def equip_item_ajax(request, item_id):
    """
    AJAX View: Equip an item via drag-and-drop interaction.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.avatar

    if avatar.equipped_items.filter(id=item.id).exists():
        avatar.unequip_item(item)
        status = "unequipped"
    else:
        avatar.equip_item(item)
        status = "equipped"

    return JsonResponse({
        'status': status,
        'item_id': item_id,
        'message': f"{item.name} has been {status}.",
        'image_url': static(item.image_path)
    })


@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Handles the purchase of an item for the user's avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.avatar
    user = request.user

    if item.premium_only and not user.is_premium():
        messages.error(request, "This item is for premium users only.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    if PurchasedItem.objects.filter(user=user, item=item).exists():
        messages.info(request, "You have already purchased this item.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    if item.price_points and user.points < item.price_points:
        messages.error(
            request, "You do not have enough points to purchase this item.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    user.deduct_points(item.price_points)
    PurchasedItem.objects.create(user=user, item=item)
    messages.success(request, f"You have successfully purchased {item.name}!")

    return redirect('dressup:shop_detail', shop_id=item.shop.id)


@login_required
@avatar_required
def unequip_item(request, item_id):
    """
    Unequips an item from the avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.avatar

    if item in avatar.equipped_items.all():
        avatar.unequip_item(item)
        messages.success(
            request, f"{item.name} has been successfully unequipped.")
    else:
        messages.error(request, f"{item.name} is not equipped.")

    return redirect('dressup:inventory')
