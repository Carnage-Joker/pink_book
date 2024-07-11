
from .models import Avatar, ClothingItem
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Avatar, PremiumOutfit, Pose, Environment, Feature, Favorites, ClothingItem
from .forms import AvatarForm
from journal.models import CustomUser


@csrf_exempt
def save_avatar(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        avatar, created = Avatar.objects.get_or_create(user=user)
        avatar.body_type = data['body_type']
        avatar.skin_tone = data['skin_tone']
        avatar.hair_type = data['hair_type']
        avatar.hair_color = data['hair_color']
        avatar.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def dress_up_game(request):
    avatar = Avatar.objects.get(user=request.user)

    if not avatar:
        return redirect('virtual_try_on:avatar_customization')

    tops = ClothingItem.objects.filter(category='top', is_premium=False)
    skirts = ClothingItem.objects.filter(category='skirt', is_premium=False)
    dresses = ClothingItem.objects.filter(category='dress', is_premium=False)
    shoes = ClothingItem.objects.filter(category='shoes', is_premium=False)

    if avatar.top:
        tops = tops.exclude(id=avatar.top.id)[:2]
    else:
        tops = tops[:2]

    if avatar.skirt:
        skirts = skirts.exclude(id=avatar.skirt.id)[:2]
    else:
        skirts = skirts[:2]

    if avatar.dress:
        dresses = dresses.exclude(id=avatar.dress.id)[:2]
    else:
        dresses = dresses[:2]

    if avatar.shoes:
        shoes = shoes.exclude(id=avatar.shoes.id)[:2]
    else:
        shoes = shoes[:2]

    context = {
        'avatar': avatar,
        'body_image_path': avatar.get_body_image_path(),
        'hair_image_path': avatar.get_hair_image_path(),
        'top_image_path': avatar.get_top_image_path(),
        'skirt_image_path': avatar.get_skirt_image_path(),
        'dress_image_path': avatar.get_dress_image_path(),
        'shoes_image_path': avatar.get_shoes_image_path(),
        'tops': tops,
        'skirts': skirts,
        'dresses': dresses,
        'shoes': shoes,
    }
    return render(request, 'virtual_try_on/dress_up_game.html', context)




# logic to check if user has an avatar saved, if not redirect them to avatar_customization.html
def has_saved_avatar(user):
    try:
        avatar = Avatar.objects.get(user=user)
    except Avatar.DoesNotExist:
        return False
    return True


def premium_outfit_list(request):
    outfits = PremiumOutfit.objects.all()
    return render(request, 'virtual_try_on/premium_outfit_list.html', {'outfits': outfits})

# View to handle the avatar customization page


# virtual_try_on/views.py


@login_required
def avatar_customization(request):
    avatar, _ = Avatar.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=avatar)
        if form.is_valid():
            form.save()
            return redirect('virtual_try_on:dress_up_game')
    else:
        form = AvatarForm(instance=avatar)

    clothing_items = ClothingItem.objects.filter(is_premium=False)
    context = {
        'avatar': avatar,
        'form': form,
        'body_image_path': avatar.get_body_image_path(),
        'hair_image_path': avatar.get_hair_image_path(),
        'top_image_path': avatar.get_top_image_path(),
        'skirt_image_path': avatar.get_skirt_image_path(),
        'dress_image_path': avatar.get_dress_image_path(),
        'shoes_image_path': avatar.get_shoes_image_path(),
        'clothing_items': clothing_items,
    }
    return render(request, 'virtual_try_on/avatar_customization.html', context)


@csrf_exempt
def update_avatar_feature(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            feature_type = data.get('feature_type')
            feature_value = data.get('feature_value')

            avatar = Avatar.objects.get(user=request.user)

            if feature_type == 'body':
                avatar.body_type = feature_value.split('/')[1]
                avatar.skin_tone = feature_value.split('/')[0]
            elif feature_type == 'hair':
                avatar.hair_type = feature_value.split('/')[0]
                avatar.hair_color = feature_value.split('/')[1]

            avatar.save()
            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Avatar.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Avatar not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@login_required
def toggle_favorite_outfit(request, pk):
    outfit = get_object_or_404(PremiumOutfit, pk=pk)
    favorite, created = Favorites.objects.get_or_create(
        user=request.user, outfit=outfit)
    if not created:
        favorite.delete()
        return JsonResponse({'action': 'removed'})
    return JsonResponse({'action': 'added'})


@login_required
def favorite_outfits_list(request):
    favorites = Favorites.objects.filter(user=request.user)
    return render(request, 'virtual_try_on/favorite_outfits_list.html', {'favorites': favorites})


@login_required
def my_avatar(request):
    avatar = get_object_or_404(Avatar, user=request.user)
    outfit = avatar.get_outfit()
    return render(request, 'virtual_try_on/my_avatar.html', {'avatar': avatar, 'outfit': outfit})
