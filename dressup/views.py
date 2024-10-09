from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import Avatar, ClothingItem, FavoriteOutfit, PhotoshootLocation, Item, PurchasedItem

# CreateAvatarView


@method_decorator(login_required, name='dispatch')
class CreateAvatarView(View):
    def get(self, request):
        if Avatar.objects.filter(user=request.user).exists():
            messages.info(request, "You already have an avatar!")
            return redirect('dressup:avatar_exists')
        return render(request, 'create_avatar.html')

    def post(self, request):
        user = request.user
        if Avatar.objects.filter(user=user).exists():
            messages.info(request, "You already have an avatar!")
            return redirect('dressup:avatar_exists')

        avatar = Avatar.objects.create(user=user)
        messages.success(request, "Your avatar has been created!")
        return redirect('dressup:avatar_created')


# DressUpView - Display Avatar and Available Clothing Items
@method_decorator(login_required, name='dispatch')
class DressUpView(View):
    def get(self, request):
        avatar = get_object_or_404(Avatar, user=request.user)
        clothing_items = ClothingItem.objects.all()
        return render(request, 'my_avatar.html', {
            'avatar': avatar,
            'clothing_items': clothing_items,
        })


# PurchasePremiumOutfitView - Allow Premium Users to Purchase Outfits
@method_decorator(login_required, name='dispatch')
class PurchasePremiumOutfitView(View):
    def post(self, request, outfit_id):
        user = request.user
        outfit = get_object_or_404(ClothingItem, id=outfit_id, is_premium=True)

        # Check if the user has a premium subscription
        if not hasattr(user, 'billing') or user.billing.subscription_status != 'premium':
            messages.error(
                request, "You need a premium subscription to purchase this outfit.")
            return redirect('dressup:premium_outfit_list')

        # Add the outfit to user's collection
        PurchasedItem.objects.create(user=user, item=outfit)
        messages.success(
            request, f"{outfit.name} has been added to your collection!")
        return redirect('dressup:favorite_outfit_list')


# FavoriteOutfitListView - Display User's Favorite Outfits
@method_decorator(login_required, name='dispatch')
class FavoriteOutfitListView(View):
    def get(self, request):
        favorite_outfits = FavoriteOutfit.objects.filter(user=request.user)
        return render(request, 'favorite_outfit_list.html', {
            'favorite_outfits': favorite_outfits,
        })


# PhotoshootLocationView - Select Photoshoot Locations for Avatars
@method_decorator(login_required, name='dispatch')
class PhotoshootLocationView(View):
    def get(self, request):
        locations = PhotoshootLocation.objects.all()
        return render(request, 'mall.html', {
            'locations': locations,
        })

    def post(self, request, location_id):
        location = get_object_or_404(PhotoshootLocation, id=location_id)

        # Check if the location is premium
        if location.is_premium and not hasattr(request.user, 'billing') or request.user.billing.subscription_status != 'premium':
            messages.error(
                request, "This photoshoot location is for premium users only.")
            return redirect('dressup:mall')

        messages.success(request, f"You've selected the {
                         location.name} for your photoshoot!")
        return redirect('dressup:photoshoot_selected', location_id=location.id)


# Create Avatar Function-Based View
@login_required
def create_avatar(request):
    user = request.user
    avatar, created = Avatar.objects.get_or_create(user=user)
    if created:
        messages.success(request, "Your avatar has been created!")
        return redirect('dressup:dress_up')
    else:
        messages.info(request, "You already have an avatar!")
        return redirect('dressup:avatar_exists')


# Dress Up Function-Based View
@login_required
def dress_up(request):
    avatar = get_object_or_404(Avatar, user=request.user)
    clothing_items = ClothingItem.objects.all()
    return render(request, 'my_avatar.html', {'avatar': avatar, 'clothing_items': clothing_items})


# Purchase Item View for Buying Clothing Items
@login_required
def purchase_item(request, item_id):
    item = get_object_or_404(ClothingItem, id=item_id)

    # Check for Premium Item Restriction
    if item.is_premium and not hasattr(request.user, 'billing') or request.user.billing.subscription_status != 'premium':
        messages.error(
            request, "You need a premium subscription to purchase this item.")
        return redirect('dressup:mall')

    # Purchase the Item
    PurchasedItem.objects.create(user=request.user, item=item)
    messages.success(request, f"You have successfully purchased {item.name}!")
    return redirect('dressup:mall')


# Mall View - Display Items Available for Purchase
@login_required
def mall(request):
    premium_only = hasattr(
        request.user, 'billing') and request.user.billing.subscription_status == 'premium'
    items = ClothingItem.objects.filter(
        is_premium=False) if not premium_only else ClothingItem.objects.all()
    return render(request, 'mall.html', {'items': items})


# Avatar Created Page
def avatar_created(request):
    return render(request, 'avatar_created.html')


# Avatar Exists Page
def avatar_exists(request):
    return render(request, 'avatar_exists.html')


