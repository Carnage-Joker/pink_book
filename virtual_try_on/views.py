from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .models import Avatar, PremiumOutfit, Pose, Environment, Feature, Favorites
from .forms import AvatarForm

# View to list all premium outfits


def premium_outfit_list(request):
    outfits = PremiumOutfit.objects.all()
    return render(request, 'virtual_try_on/premium_outfit_list.html', {'outfits': outfits})

# View to detail a specific premium outfit




# View to handle the avatar customization page


# virtual_try_on/views.py

@login_required
def avatar_customization(request):
    avatar, _ = Avatar.objects.get_or_create(user=request.user)
    poses = Pose.objects.all()
    environments = Environment.objects.all()
    features = Feature.objects.all()


    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=avatar)
        if form.is_valid():
            form.save()
            # Use namespace here
            return redirect('virtual_try_on:avatar_customization')
    else:
        form = AvatarForm(instance=avatar)

    context = {
        'avatar': avatar,
        'form': form,
        'poses': poses,
        'environments': environments,
        'features': features,
    }
    return render(request, 'virtual_try_on/avatar_customization.html', context)


@csrf_exempt
def update_avatar_feature(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        _ = data.get('feature_type')
        _ = data.get('feature_value')

        # Update the avatar based on feature_type and feature_value
        # For demonstration, we assume it's successful
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@login_required
def toggle_favorite_outfit(request, pk):
    outfit = get_object_or_404(PremiumOutfit, pk=pk)
    favorite, created = Favorites.objects.get_or_create(
        user=request.user, outfit=outfit)
    if not created:
        favorite.delete()
        return JsonResponse({'action': 'removed'})
    return JsonResponse({'action': 'added'})

# View to list user's favorite outfits


@login_required
def favorite_outfits_list(request):
    favorites = Favorites.objects.filter(user=request.user)
    return render(request, 'virtual_try_on/favorite_outfits_list.html', {'favorites': favorites})

# View to display user's saved avatar


@login_required
def my_avatar(request):
    avatar = get_object_or_404(Avatar, user=request.user)
    return render(request, 'virtual_try_on/my_avatar.html', {'avatar': avatar})
