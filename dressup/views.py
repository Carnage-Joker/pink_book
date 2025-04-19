# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

from .decorators import avatar_required
from .forms import AvatarCreationForm
from .models import Avatar, Item, PurchasedItem, Shop
from .utils import sassy_info, sassy_error, sassy_success

# Constants
AVATAR_LAYERS = ['body', 'skirt', 'top', 'shoes', 'hair', 'accessories']
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


@login_required
@avatar_required
def inventory_view(request: HttpRequest):
    avatar = request.user.sissy_avatar
    purchased_items = PurchasedItem.objects.filter(
        user=request.user).select_related('item')

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if item in avatar.equipped_items.all():
            avatar.unequip_item(item)
            sassy_success(
                request, f"{item.name} has been unequipped, darling!")
        else:
            avatar.equip_item(item)
            sassy_success(request, f"{item.name} is fabulously equipped!")

        return redirect('dressup:inventory')

    context = {
        'avatar': avatar,
        'purchased_items': purchased_items,
        'equipped_items': avatar.equipped_items.all(),
        'layer_keys': AVATAR_LAYERS,
        'image_urls': avatar.get_image_urls(),
        'category_choices': {
            'hair': ['00', '01', '02'],
            'top': ['00', '01', '02'],
            'skirt': ['00', '01', '02'],
            'shoes': ['00', '01', '02'],
            'accessories': ['00', '01', '02']
        },
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
        'item_id': item_id,
        'message': f"{item.name} is now {status}!",
        'image_url': static(item.image_path)
    })
@login_required
@avatar_required
