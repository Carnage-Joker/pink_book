from collections import defaultdict
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
    if not avatar:
        sassy_error(request, "You need to create an avatar first, darling!")
        return redirect('dressup:create_avatar')
    item = get_object_or_404(Item, id=item_id)

    if item.premium_only and not getattr(request.user, 'is_premium', False):
        sassy_error(
            request, "Sorry darling, this item is for premium members only.")
        return redirect('dressup:mall')

    if PurchasedItem.objects.filter(avatar=avatar, item=item).exists():
        sassy_info(request, "You already own this fabulous item!")
    else:
        PurchasedItem.objects.create(avatar=avatar, item=item)
        sassy_success(request, f"{item.name} added to your closet!")

    shop = item.shop if item.shop else None
    if shop:
        sassy_info(request, f"Thank you for shopping at {shop.name}!")
    return redirect('dressup:shop_detail', shop_id=shop.id if shop else 'dressup:mall')


# views.py

@login_required
@avatar_required
def inventory_view(request: HttpRequest) -> HttpResponse:
    avatar = request.user.sissy_avatar
    purchased_qs = PurchasedItem.objects.filter(avatar=avatar)


    paginator = Paginator(purchased_qs, 10)
    purchased_page = paginator.get_page(request.GET.get('page'))
    equipped_item_ids = set(avatar.equipped_items.values_list('id', flat=True))

    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        # Equip/unequip toggle
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            if item.id in equipped_item_ids:
                avatar.unequip_item(item)
                sassy_info(request, f"{item.name} has been unequipped.")
            else:
                avatar.equip_item(item)
                sassy_success(request, f"{item.name} is now equipped!")
            return redirect('dressup:inventory')

        # Save outfit with a name
        elif 'save_outfit' in request.POST:
            from .models import SavedOutfit
            outfit_name = request.POST.get('outfit_name', 'My Fabulous Look')

            SavedOutfit.objects.create(
                user=request.user,
                name=outfit_name.strip() or 'Unnamed Look',
                top=request.POST.get('top', '00'),
                skirt=request.POST.get('skirt', '00'),
                shoes=request.POST.get('shoes', '00'),
                accessory=request.POST.get('accessory', '00'),
            )
            sassy_success(request, f"Saved your outfit as “{outfit_name}”! 💖")

        elif 'fav_outfit' in request.POST:
            sassy_info(request, "Favoriting outfits is coming soon, darling!")

        else:
            sassy_error(request, "Nothing selected – please try again.")
        return redirect('dressup:inventory')

    equipped_map = defaultdict(lambda: '00')
    for item in avatar.equipped_items.all():
        equipped_map[item.category] = item.name  # or a code if you store it

    context = {
        'avatar': avatar,
        'purchased_items': purchased_page,
        'equipped_items': avatar.equipped_items.all(),
        'layer_keys': ['body', 'hair', 'skirt', 'top', 'shoes', 'accessories'],
        'image_urls': avatar.get_image_urls(),
        'categories': ['hair', 'top', 'skirt', 'shoes', 'accessory'],
        'equipped_map': dict(equipped_map),
    }

    return render(request, 'dressup/inventory.html', context)


@login_required
@avatar_required
@login_required
@avatar_required
def equip_item_ajax(request: HttpRequest, item_id: int) -> JsonResponse:
    avatar = request.user.sissy_avatar
    item = get_object_or_404(Item, id=item_id)

    # Ownership check
    if not PurchasedItem.objects.filter(avatar=avatar, item=item).exists():
        return JsonResponse({
            'status': 'error',
            'message': "You don't own this item!",
        }, status=403)

    # Equip or unequip
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
