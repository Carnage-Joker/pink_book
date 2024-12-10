from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from journal.models import CustomUser

from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    View to handle the creation of a new Avatar for the logged-in user.
    Allows selection of skin tone and body type. Sets default values for
    other attributes and redirects to the mall after creation.
    """
    # Check if the user already has an avatar
    if hasattr(request.user, 'avatar'):
        messages.info(
            request, "You already have an avatar. Redirecting to the mall.")
        return redirect('dressup:mall')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user
            # Set default values for other attributes
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

    context = {
        'form': form,
    }
    return render(request, 'dressup/create_avatar.html', context)


@login_required
@avatar_required
def mall_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the mall where users can upgrade their avatars.
    """
    shops = Shop.objects.all()
    # Use the related_name for the avatar relationship
    avatar = getattr(request.user, 'sissy_avatar', None)

    if avatar is None:
        # Optionally, redirect the user to an avatar creation page
        messages.error(request, "You need to create an avatar first!")
        # Replace with your actual URL name for avatar creation
        return redirect('dressup:create_avatar')

    # Correct call to get_image_urls
    image_urls = avatar.get_image_urls()
    equipped_items = avatar.equipped_items.all()

    context = {
        'shops': shops,
        'avatar': avatar,
        'image_urls': image_urls,
        'equipped_items': equipped_items,  # Include equipped items
    }
    return render(request, 'dressup/mall.html', context)


@login_required
@avatar_required
def shop_detail(request: HttpRequest, shop_id: int) -> HttpResponse:
    """
    Displays details of a specific shop and handles item purchases.
    """
    shop = get_object_or_404(Shop, id=shop_id)
    items = Item.objects.filter(shop=shop)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id, shop=shop)
        avatar = request.user.avatar

        # Check if the item is already purchased
        if PurchasedItem.objects.filter(avatar=avatar, item=item).exists():
            messages.info(request, "You have already purchased this item.")
        else:
            # Create a PurchasedItem entry
            PurchasedItem.objects.create(avatar=avatar, item=item)
            messages.success(
                request, f"You have successfully purchased {item.name}!")
            return redirect('dressup:mall')

    context = {
        'shop': shop,
        'items': items,
    }
    return render(request, 'dressup/shop_detail.html', context)


@login_required
def equip_item(self, item):
    """
    Equip an item to the avatar, ensuring only one item per category is equipped.
    """
    # Check if the item has a category
    if hasattr(item, 'category'):
        # Unequip currently equipped item in the same category
        current_item = self.equipped_items.filter(
            category=item.category).first()
        if current_item:
            self.equipped_items.remove(current_item)

    # Equip the new item
    self.equipped_items.add(item)
    self.save()


@login_required
@avatar_required
def unequip_item(self, item):
    """
    Unequip an item from the avatar.
    """
    if item in self.equipped_items.all():
        self.equipped_items.remove(item)
        self.save()
    else:
        raise ValueError(f"The item {item.name} is not currently equipped.")


@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Handles the purchase of an item for the user's avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.avatar
    user = request.user

    # Check if the item is premium-only and the user isn't a premium subscriber
    if item.premium_only and not user.is_premium():
        messages.error(request, "This item is for premium users only.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    # Check if the user already owns the item
    if PurchasedItem.objects.filter(avatar=avatar, item=item).exists():
        messages.info(request, "You have already purchased this item.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    # Check if the user has enough points or dollars
    if item.price_points and user.points < item.price_points:
        messages.error(
            request, "You do not have enough points to purchase this item.")
        return redirect('dressup:shop_detail', shop_id=item.shop.id)

    # Deduct points and complete the purchase
    if item.price_points:
        user.deduct_points(item.price_points)

    # Optional: Implement real money logic if item.price_dollars is set

    # Add the item to the user's purchased items
    PurchasedItem.objects.create(avatar=avatar, item=item)
    messages.success(request, f"You have successfully purchased {item.name}!")

    # Optionally award points for purchases (if desired)
    user.award_points(5)  # Example: Earn 5 points for any purchase

    return redirect('dressup:shop_detail', shop_id=item.shop.id)


@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    """
    Displays the user's purchased items and their equip status.
    """
    avatar = request.user.avatar
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    equipped_items = avatar.equipped_items.all()

    context = {
        'purchased_items': purchased_items,
        'equipped_items': equipped_items,
    }
    return render(request, 'dressup/inventory.html', context)
