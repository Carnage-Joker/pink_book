from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.templatetags.static import static

from .decorators import avatar_required
from .models import Item, PurchasedItem, Avatar, Shop
from .forms import AvatarCreationForm
from .utils import sassy_success, sassy_error, sassy_info

# Constants
STARTER_ITEMS = ["Barely Boyish", "Tight Jeans", "Tank Top", "Sneakers"]
AVATAR_LAYERS = ['body', 'hair', 'skirt', 'top', 'shoes', 'accessories']


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
            avatar.hair = form.cleaned_data['hair']
            avatar.hair_color = form.cleaned_data['hair_color']
            avatar.save()

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

    available_items = PurchasedItem.objects.filter(
        user=request.user).select_related('item')

    context = {
        'avatar': avatar,
        'image_urls': avatar.get_image_urls(),
        'layer_keys': AVATAR_LAYERS,
        'available_items': [pi.item for pi in available_items],
    }
    return render(request, 'dressup/dress_up.html', context)


@login_required
@avatar_required
def shop_detail(request: HttpRequest, shop_id: int) -> HttpResponse:
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()
    return render(request, 'dressup/shop_detail.html', {'shop': shop, 'items': items})


@login_required
@avatar_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    avatar = request.user.sissy_avatar
    item = get_object_or_404(Item, id=item_id)

    if item.premium_only and not getattr(request.user, 'is_premium', False):
        sassy_error(
            request, "Sorry darling, this item is for premium members only.")
        return redirect('dressup:mall')

    if PurchasedItem.objects.filter(user=request.user, item=item).exists():
        sassy_info(request, "You already own this fabulous item!")
    else:
        PurchasedItem.objects.create(user=request.user, item=item)
        sassy_success(request, f"{item.name} added to your closet!")

    shop = item.shop_set.first()
    return redirect('dressup:shop_detail', shop_id=shop.id if shop else 'dressup:mall')


@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    avatar = request.user.sissy_avatar
    purchased_qs = PurchasedItem.objects.filter(
        user=request.user).select_related('item')
    paginator = Paginator(purchased_qs, 10)
    purchased_page = paginator.get_page(request.GET.get('page'))
    equipped_item_ids = set(avatar.equipped_items.values_list('id', flat=True))

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            if item.id in equipped_item_ids:
                avatar.unequip_item(item)
            else:
                avatar.equip_item(item)
                sassy_success(request, f"{item.name} is now equipped!")
            return redirect('dressup:inventory')

        elif 'save_outfit' in request.POST:
            avatar.hair = request.POST.get('hair', avatar.hair)
            avatar.top = request.POST.get('top', avatar.top)
            avatar.skirt = request.POST.get('skirt', avatar.skirt)
            avatar.shoes = request.POST.get('shoes', avatar.shoes)
            avatar.accessory = request.POST.get('accessory', avatar.accessory)
            avatar.save()
            sassy_success(request, "Your outfit has been saved!")

        elif 'fav_outfit' in request.POST:
            avatar.favourite_top = avatar.top
            avatar.favourite_skirt = avatar.skirt
            avatar.favourite_shoes = avatar.shoes
            avatar.favourite_accessory = avatar.accessory
            avatar.save()
            sassy_success(request, "Favourite outfit updated!")

        else:
            sassy_error(request, "Nothing selected – please try again.")
        return redirect('dressup:inventory')

    context = {
        'avatar': avatar,
        'purchased_items': purchased_page,
        'equipped_items': avatar.equipped_items.all(),
        'layer_keys': AVATAR_LAYERS,
        'image_urls': avatar.get_image_urls(),
        'categories': ['hair', 'top', 'skirt', 'shoes', 'accessory'],
    }
    return render(request, 'dressup/inventory.html', context)


@login_required
@avatar_required
def equip_item_ajax(request: HttpRequest, item_id: int) -> JsonResponse:
    avatar = request.user.sissy_avatar
    item = get_object_or_404(Item, id=item_id)

    if avatar.equipped_items.filter(id=item.id).exists():
        avatar.unequip_item(item)
        status = "unequipped"
    else:
        avatar.equip_item(item)
        status = "equipped"

    return JsonResponse({
        'status': status,
        'item_id': item.id,
        'category': item.category,
        'image_url': static(item.image_path) if item.image_path else "",
        'message': f"{item.name} is now {status}!",
    })
