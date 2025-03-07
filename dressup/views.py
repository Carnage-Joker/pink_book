from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop
from django.templatetags.static import static
# Import our custom message functions
from .utils import sassy_info, sassy_error, sassy_success

# Constants
STARTER_ITEMS = ["Barely Boyish", "Tight Jeans", "Tank Top", "Sneakers"]


def handle_existing_avatar(request, avatar):
    """
    Helper function to redirect if an avatar already exists.
    """
    if not avatar.story_started:
        sassy_info(
            request, "You already have an avatar. Redirecting to your story introduction!")
        return redirect('dressup:story_intro')
    else:
        sassy_error(
            request, "You already have an avatar. Redirecting to the mall!")
        return redirect('dressup:mall')


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    Creates a new avatar for the user if one does not already exist.
    """
    avatar, created = Avatar.objects.get_or_create(user=request.user)

    # If the avatar already exists, handle redirection with a sassy message.
    if not created:
        return handle_existing_avatar(request, avatar)

    # Process POST request for avatar customization.
    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar.body = form.cleaned_data['body']
            avatar.skin = form.cleaned_data['skin']
            avatar.save()

            # Equip the default starter outfit.
            for item_name in STARTER_ITEMS:
                item = Item.objects.filter(name=item_name).first()
                if item:
                    avatar.equip_item(item)

            sassy_success(
                request, "Your avatar has been created with a fab default outfit!")
            return redirect('dressup:story_intro')
        else:
            sassy_error(request, "Please correct the errors below, darling!")
    else:
        form = AvatarCreationForm()

    return render(request, 'dressup/create_avatar.html', {'form': form})


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
    sassy_success(request, "Your avatar is ready for a fabulous adventure!")
    return render(request, 'dressup/story_intro.html')


@login_required
@avatar_required
def mall_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the mall with shop listings and the current state of the avatar.
    """
    avatar = request.user.sissy_avatar
    layer_keys = ['body', 'skirt', 'top', 'shoes', 'hair', 'accessories']
    image_urls = avatar.get_image_urls() if avatar else {}

    shops = Shop.objects.all().order_by('id')
    paginator = Paginator(shops, 10)
    page_number = request.GET.get('page')
    shops_page = paginator.get_page(page_number)

    context = {
        'shops': shops_page,
        'avatar': avatar,
        'image_urls': image_urls,
        'layer_keys': layer_keys,
    }
    return render(request, 'dressup/mall.html', context)


@login_required
@avatar_required
def dress_up_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the interactive dress-up page.
    """
    avatar = request.user.sissy_avatar
    if request.method == 'POST':
        # Process outfit changes here (via AJAX or form submission)
        sassy_success(request, "Your outfit has been saved, looking chic!")
        return redirect('dressup:mall')
    return render(request, 'dressup/dress_up.html', {'avatar': avatar})


@login_required
@avatar_required
def shop_detail(request: HttpRequest, shop_id: int) -> HttpResponse:
    """
    Displays details of a specific shop and handles item purchases.
    """
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(shop.items, id=item_id)
        if PurchasedItem.objects.filter(user=request.user, item=item).exists():
            sassy_info(request, "You already own this fabulous item!")
        else:
            PurchasedItem.objects.create(user=request.user, item=item)
            sassy_success(request, f"You have snagged {item.name}! Enjoy!")
            return redirect('dressup:mall')

    return render(request, 'dressup/shop_detail.html', {'shop': shop, 'items': items})


@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the user's purchased items and allows equipping/unequipping.
    """
    avatar = request.user.sissy_avatar
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    equipped_items = avatar.equipped_items.all()

    if request.method == 'POST' or request.GET.get('item_id'):
        item_id = request.POST.get('item_id') or request.GET.get('item_id')
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            sassy_error(request, "Oops! That item doesn't exist, sweetie!")
            return redirect('dressup:inventory')

        if item in equipped_items:
            avatar.unequip_item(item)
            sassy_success(
                request, f"{item.name} has been unequipped. Mix it up!")
        else:
            avatar.equip_item(item)
            sassy_success(
                request, f"{item.name} is now on point and equipped!")

    context = {
        'purchased_items': purchased_items,
        'equipped_items': avatar.equipped_items.all(),
    }
    return render(request, 'dressup/inventory.html', context)


@login_required
@avatar_required
def equip_item_ajax(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    AJAX view: Toggles equipping or unequipping an item.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.sissy_avatar

    if avatar.equipped_items.filter(id=item.id).exists():
        avatar.unequip_item(item)
        status = "unequipped"
    else:
        avatar.equip_item(item)
        status = "equipped"

    return JsonResponse({
        'status': status,
        'item_id': item_id,
        'message': f"{item.name} has been {status}!",
        'image_url': static(item.image_path)
    })


@login_required
@avatar_required
def unequip_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Unequips an item from the avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.sissy_avatar

    if item in avatar.equipped_items.all():
        avatar.unequip_item(item)
        sassy_success(request, f"{item.name} has been unequipped!")
    else:
        sassy_error(request, f"{item.name} isn't even equipped, darling!")
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
        sassy_error(request, "This item is for premium users only, sweetie!")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    if PurchasedItem.objects.filter(user=user, item=item).exists():
        sassy_info(request, "You've already purchased this stylish item!")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    if item.price_points and user.points < item.price_points:
        sassy_error(
            request, "Not enough points, darling. Time to earn more sparkle!")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    user.deduct_points(item.price_points)
    PurchasedItem.objects.create(user=user, item=item)
    sassy_success(
        request, f"You have successfully purchased {item.name}! Enjoy your new look!")
    return redirect('dressup:shop_detail', shop_id=item.shop.id)
