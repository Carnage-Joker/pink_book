from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page

from .models import Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required
from .utils import handle_error  # Centralized error handling


@cache_page(60 * 15)  # Cache for 15 minutes
@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    View to handle the creation of a new Avatar for the logged-in user.
    Simplified to only allow selection of skin tone and body type.
    Sets default values for other attributes.
    Redirects to the mall after creation.
    """
    # Check if the user already has an avatar
    if hasattr(request.user, 'avatar'):
        return handle_error(request, "You already have an avatar. Redirecting to the mall.", 'dressup:mall')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user
            # Set default values
            avatar.hair = '00'
            avatar.hair_color = '00'
            avatar.shoes = '00'
            avatar.accessories = '00'
            avatar.skirt = '00'
            avatar.top = '00'
            avatar.name = f"{request.user.sissy_name}'s Avatar"
            avatar.save()
            messages.success(
                request, "Your avatar has been created successfully!")
            return redirect('dressup:mall')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AvatarCreationForm()

    context = {'form': form}
    return render(request, 'dressup/create_avatar.html', context)


@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Handles purchasing an item for the user's avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    user = request.user

    # Check if item is premium-only and user is not premium
    if item.premium_only and not user.is_premium():
        return handle_error(request, "This item is for premium users only.", 'dressup:shop_detail', {'shop_id': item.shop.id})

    # Check if user has enough points or money
    if item.price_points and user.points < item.price_points:
        return handle_error(request, "You do not have enough points to purchase this item.", 'dressup:shop_detail', {'shop_id': item.shop.id})

    # Deduct points or handle payment
    if item.price_points:
        user.deduct_points(item.price_points)
        PurchasedItem.objects.create(user=user, item=item)
        messages.success(request, f"You have purchased {item.name}!")
        return redirect('dressup:inventory')

    # Payment gateway logic for real money purchases
    # ...

    return handle_error(request, "An unexpected error occurred. Please try again.", 'dressup:shop_detail', {'shop_id': item.shop.id})


@login_required
@avatar_required
def equip_item_ajax(request, item_id: int) -> JsonResponse:
    """
    AJAX View: Equip an item via drag-and-drop interaction.
    """
    item = get_object_or_404(Item, id=item_id)
    status = request.user.avatar.toggle_item(item)
    return JsonResponse({'status': status, 'message': f"Item {status} successfully."})


@login_required
@avatar_required
def mall_view(request: HttpRequest) -> HttpResponse:
    """
    View to display the mall where users can upgrade their avatars.
    """
    shops = Shop.objects.all()
    avatar = request.user.avatar
    image_urls = avatar.get_image_urls()
    context = {'shops': shops, 'avatar': avatar, 'image_urls': image_urls}
    return render(request, 'dressup/mall.html', context)


@login_required
@avatar_required
def shop_detail(request: HttpRequest, shop_id: int) -> HttpResponse:
    """
    View to display details of a specific shop.
    """
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()
    context = {'shop': shop, 'items': items}
    return render(request, 'dressup/shop_detail.html', context)


@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    """
    View to display the user's inventory of purchased items.
    """
    avatar = request.user.avatar
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    equipped_items = avatar.equipped_items.all()

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if item in equipped_items:
            avatar.unequip_item(item)
            messages.success(request, f"{item.name} has been unequipped.")
        else:
            avatar.equip_item(item)
            messages.success(request, f"{item.name} has been equipped.")

    context = {'purchased_items': purchased_items,
               'equipped_items': equipped_items}
    return render(request, 'dressup/inventory.html', context)
