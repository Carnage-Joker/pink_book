# views.py

from .models import Item, PurchasedItem, Shop
from django.shortcuts import get_object_or_404, redirect
from .decorators import avatar_required
from .utils import sassy_success, sassy_error, sassy_info
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# Removed redundant import of sassy_success
from django.templatetags.static import static
from .models import Item, PurchasedItem, Avatar, Shop
from django.contrib.auth.decorators import login_required
from .forms import AvatarCreationForm
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect, render, get_object_or_404


# Constants
# Defines the layers used for avatar customization
# List of default items assigned to a new avatar
STARTER_ITEMS = ["Barely Boyish", "Tight Jeans", "Tank Top", "Sneakers"]


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    avatar, created = Avatar.objects.get_or_create(user=request.user)

    if not created:
        if avatar.story_started:
            sassy_info(
                request, "You already have an avatar. Let's hit the mall!")
            return redirect('dressup:mall')
        sassy_info(request, "Redirecting to your fabulous story introduction!")
        return redirect('dressup:story_intro')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            avatar.body = form.cleaned_data['body']
            avatar.skin = form.cleaned_data['skin']
            avatar.save()

            # Equip the default starter outfit safely
            starter_items = ["Barely Boyish",
                             "Tight Jeans", "Tank Top", "Sneakers"]
            for item_name in STARTER_ITEMS:
                item = Item.objects.filter(name=item_name).first()
                if item:
                    avatar.equip_item(item)

            sassy_success(
                request, "Avatar created with a fabulous starter outfit!")
            return redirect('dressup:story_intro')
        else:
            sassy_error(request, "Please fix those tiny issues below!")
    else:
        form = AvatarCreationForm()

    return render(request, 'dressup/create_avatar.html', {'form': form})


@login_required
@avatar_required
def story_intro_view(request: HttpRequest) -> HttpResponse:
    avatar = request.user.sissy_avatar
    if not avatar.story_started:
        avatar.story_started = True
        avatar.save()
    sassy_success(request, "Your adventure begins now, darling!")
    return render(request, 'dressup/story_intro.html')


@login_required
@avatar_required
def mall_view(request: HttpRequest) -> HttpResponse:
    avatar = request.user.sissy_avatar
    shops = Shop.objects.all().order_by('id')
    paginator = Paginator(shops, 10)
    shops_page = paginator.get_page(request.GET.get('page'))

    context = {
        'shops': shops_page,
        'avatar': avatar,
        'image_urls': avatar.get_image_urls(),
        'layer_keys': AVATAR_LAYERS,
    }
    return render(request, 'dressup/mall.html', context)


@login_required
@avatar_required
def dress_up_view(request: HttpRequest) -> HttpResponse:
    avatar = request.user.sissy_avatar

    if request.method == 'POST':
        avatar.top = request.POST.get('top', '00')
        avatar.skirt = request.POST.get('skirt', '00')
        avatar.shoes = request.POST.get('shoes', '00')
        avatar.accessory = request.POST.get('accessory', '00')
        avatar.save()
        sassy_success(request, "Your new look is stunning, sweetie!")
        return redirect('dressup:mall')

    context = {
        'avatar': avatar,
        'image_urls': avatar.get_image_urls(),
        'layer_keys': AVATAR_LAYERS,
    }
    return render(request, 'dressup/dress_up.html', context)


@login_required
@avatar_required
def shop_detail(request: HttpRequest, shop_id: int) -> HttpResponse:
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()

    if request.method == 'POST':
        item = get_object_or_404(Item, id=request.POST.get('item_id'))
        if PurchasedItem.objects.filter(user=request.user, item=item).exists():
            sassy_info(request, "You already own that beauty!")
        else:
            PurchasedItem.objects.create(user=request.user, item=item)
            sassy_success(
                request, f"{item.name} is yours now! Fabulous choice!")
            return redirect('dressup:mall')

    return render(request, 'dressup/shop_detail.html', {'shop': shop, 'items': items})


# dressup/views.py  ──────────────────────────────────────────────────────────


@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    """
    Closet page:
      • shows paginated purchased items
      • live‑preview next/prev cycling (handled in JS)
      • POST              item_id   → equip / unequip
      • POST save_outfit  + hidden  → update avatar.<field> codes
      • POST fav_outfit            → mark current codes as favourite
    """
    avatar = request.user.sissy_avatar

    # ------------------------------------------------------------------ pagination
    purchased_qs = PurchasedItem.objects.filter(
        user=request.user).select_related('item')
    paginator = Paginator(purchased_qs, 10)
    purchased_page = paginator.get_page(request.GET.get('page'))

    equipped_item_ids = set(avatar.equipped_items.values_list('id', flat=True))

    # ------------------------------------------------------------------ POST logic
    if request.method == 'POST':
        # 1) toggle equip / unequip via thumbnail button
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            if item.id in equipped_item_ids:
                avatar.unequip_item(item)
                sassy_success(request, f"{item.name} has been unequipped!")
            else:
                avatar.equip_item(item)
                sassy_success(request, f"{item.name} is now equipped!")
            equipped_item_ids = set(
                avatar.equipped_items.values_list('id', flat=True))  # refresh

        # 2) direct‑code outfit save (next/prev arrows)
        elif 'save_outfit' in request.POST:
            avatar.hair = request.POST.get('hair',      avatar.hair)
            avatar.top = request.POST.get('top',       avatar.top)
            avatar.skirt = request.POST.get('skirt',     avatar.skirt)
            avatar.shoes = request.POST.get('shoes',     avatar.shoes)
            avatar.accessory = request.POST.get('accessory', avatar.accessory)
            avatar.save()
            sassy_success(request, "Your outfit has been saved!")

        # 3) favourite button (very simple example)
        elif 'fav_outfit' in request.POST:
            avatar.favourite_top = avatar.top
            avatar.favourite_skirt = avatar.skirt
            avatar.favourite_shoes = avatar.shoes
            avatar.favourite_accessory = avatar.accessory
            avatar.save()
            sassy_success(request, "Favourite outfit updated!")

        else:
            sassy_error(request, "Nothing selected – please try again.")
# Removed duplicate definition of inventory_view
        return redirect('dressup:inventory')

# ------------------------------------------------------------------ context
    context = {
        'avatar': avatar,

        'purchased_items': purchased_page,
        'equipped_items': avatar.equipped_items.all(),
        'layer_keys': ['body', 'hair', 'skirt', 'top', 'shoes', 'accessories'],
        'image_urls': avatar.get_image_urls(),
        # add this line ↓↓↓
        'categories': ['hair', 'top', 'skirt', 'shoes', 'accessory'],
    }
    return render(request, 'dressup/inventory.html', context)
# dressup/views.py  ──────────────────────────────────────────────────────────


@login_required
@avatar_required
def equip_item_ajax(request: HttpRequest, item_id: int) -> JsonResponse:
    avatar = request.user.sissy_avatar
    item = get_object_or_404(Item, id=item_id)

    if avatar.equipped_items.filter(id=item.id).exists():
        status = "unequipped"
    else:
        avatar.equip_item(item)
        status = "equipped"

    return JsonResponse({
        'status': status,
        'item_id': item_id,
        'message': f"{item.name} is now {status}!",
    })


@login_required
@avatar_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, id=item_id)

    # Optional: premium check if you have such a method
    if item.premium_only and not getattr(request.user, 'is_premium', lambda: False)():
        sassy_error(
            request, "Sorry darling, this item is for premium members only.")
        return redirect('dressup:mall')

    if PurchasedItem.objects.filter(user=request.user, item=item).exists():
        sassy_info(request, "You already own this fabulous item!")
    else:
        PurchasedItem.objects.create(user=request.user, item=item)
        sassy_success(request, f"{item.name} added to your closet!")

    shop = item.shop_items.first()  # Assuming shop_items is the correct related_name
    return redirect('dressup:shop_detail', shop_id=shop.id if shop else 'dressup:mall')
