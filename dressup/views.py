from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop
from django.templatetags.static import static


from django.http import JsonResponse
from .models import Avatar


from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop
from django.templatetags.static import static


@login_required
def get_equipped_items(request):
    """ Returns a JSON response of the user's equipped avatar items. """
    avatar = request.user.sissy_avatar
    equipped_items = avatar.equipped_items.all()

    data = {}
    for category in ['body', 'hair', 'skirt', 'top', 'shoes', 'accessory']:  # Fixed category name
        category_items = list(avatar.equipped_items.filter(
            category=category).values('id', 'name', 'image_path'))
        if category_items:
            data[category] = {
                "items": category_items,
                "currentIndex": 0
            }

    return JsonResponse(data)


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new Avatar for the logged-in user.
    """
    avatar, created = Avatar.objects.get_or_create(user=request.user)

    if not created:
        if not avatar.story_started:
            return redirect('dressup:story_intro')
        else:
            messages.error(
                request, "You already have an avatar. Redirecting to the mall.")
            return redirect('dressup:mall')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar.body = form.cleaned_data['body']
            avatar.skin = form.cleaned_data['skin']
            avatar.save()

            # Equip the default starter outfit safely
            starter_items = ["Barely Boyish",
                             "Tight Jeans", "Tank Top", "Sneakers"]
            for item_name in starter_items:
                item = Item.objects.filter(name=item_name).first()
                if item:
                    avatar.equip_item(item)

            messages.success(
                request, "Your avatar has been created successfully with the default outfit!")
            return redirect('dressup:story_intro')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AvatarCreationForm()

    return render(request, 'dressup/create_avatar.html', {'form': form})


@login_required
@avatar_required
def mall_view(request):
    avatar = getattr(request.user, 'sissy_avatar', None)

    if not avatar:
        messages.error(request, "You need to create an avatar first!")
        return redirect('dressup:create_avatar')

    layer_keys = ['body', 'skirt', 'top', 'shoes', 'hair', 'accessory']
    image_urls = avatar.get_image_urls() if avatar else {}

    shops = Shop.objects.all().order_by('id')
    paginator = Paginator(shops, 10)
    page_number = request.GET.get('page')

    try:
        shops_page = paginator.get_page(page_number)
    except EmptyPage:
        shops_page = paginator.get_page(1)

    return render(request, 'dressup/mall.html', {
        'shops': shops_page,
        'avatar': avatar,
        'image_urls': image_urls,
        'layer_keys': layer_keys,
    })

@login_required
@avatar_required
def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(shop.items, id=item_id)
        avatar = request.user.sissy_avatar

        # Fixed purchase check
        if PurchasedItem.objects.filter(avatar=avatar, item=item).exists():
            messages.info(request, "You have already purchased this item.")
        else:
            PurchasedItem.objects.create(avatar=avatar, item=item)
            messages.success(
                request, f"You have successfully purchased {item.name}!")
            return redirect('dressup:mall')

    return render(request, 'dressup/shop_detail.html', {'shop': shop, 'items': items})


@login_required
@avatar_required
def equip_item_ajax(request, item_id):
    """ AJAX View: Equip an item via drag-and-drop interaction. """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.sissy_avatar

    if not item.category:
        return JsonResponse({"error": "Invalid item category"}, status=400)

    if item in avatar.equipped_items.all():
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
@avatar_required
def story_intro_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the introduction to the story mode.
    """
    avatar = request.user.sissy_avatar

    if not avatar.story_started:
        avatar.story_started = True
        avatar.save()

    messages.success(request, "Your avatar is ready for the adventure!")
    return render(request, 'dressup/story_intro.html')


@login_required
@avatar_required
def inventory_view(request):
    """
    Displays the user's purchased items and their equip status.
    """
    avatar = request.user.sissy_avatar
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    equipped_items = avatar.equipped_items.all()

    if request.method == 'POST' or request.GET.get('item_id'):
        item_id = request.POST.get('item_id') or request.GET.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if item in equipped_items:
            avatar.unequip_item(item)
            messages.success(request, f"{item.name} has been unequipped.")
        else:
            avatar.equip_item(item)
            messages.success(request, f"{item.name} has been equipped.")

    return render(request, 'dressup/inventory.html', {
        'purchased_items': purchased_items,
        'equipped_items': avatar.equipped_items.all(),
    })




@login_required
@avatar_required
def unequip_item(request, item_id):
    """
    Unequips an item from the avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.sissy_avatar

    if item in avatar.equipped_items.all():
        avatar.unequip_item(item)
        messages.success(
            request, f"{item.name} has been successfully unequipped.")
    else:
        messages.error(request, f"{item.name} is not equipped.")

    return redirect('dressup:inventory')


@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Handles the purchase of an item for the user's avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.sissy_avatar
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
