from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Avatar, PremiumOutfit, Pose, Environment, Feature, Favorites, ClothingItem
from .forms import AvatarForm

# View to list all premium outfits


@login_required
def dress_up_game(request):
    avatar = get_object_or_404(Avatar, user=request.user)
    clothing_items = ClothingItem.objects.filter(user=request.user, owned=True)

    context = {
        'avatar': avatar,
        'clothing_items': clothing_items,
        'body_image_path': avatar.get_body_image_path(),
        'hair_image_path': avatar.get_hair_image_path(),
    }
    return render(request, 'virtual_try_on/dress_up_game.html', context)


@csrf_exempt
@login_required
def update_avatar_clothing(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = data.get('category')
            src = data.get('src')

            avatar = Avatar.objects.get(user=request.user)

            if category == 'top':
                avatar.top = src
            elif category == 'bottom':
                avatar.bottom = src
            elif category == 'shoes':
                avatar.shoes = src
            elif category == 'accessory':
                avatar.accessory = src

            avatar.save()
            return JsonResponse({'success': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Avatar.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Avatar not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


def premium_outfit_list(request):
    outfits = PremiumOutfit.objects.all()
    return render(request, 'virtual_try_on/premium_outfit_list.html', {'outfits': outfits})

# View to handle the avatar customization page


@login_required
def avatar_customization(request):
    avatar, _ = Avatar.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=avatar)
        if form.is_valid():
            form.save()
            # Ensure this name matches your URL pattern
            return redirect('virtual_try_on:dress_up_game')
    else:
        form = AvatarForm(instance=avatar)

    context = {
        'avatar': avatar,
        'form': form,
        'body_image_path': avatar.get_body_image_path(),
        'hair_image_path': avatar.get_hair_image_path(),
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
