from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Avatar, Item, PurchasedItem
from journal.models import CustomUser




@login_required
def dress_up(request):
    avatar = request.user.avatar
    items = Item.objects.all()
    return render(request, 'dress_up.html', {'avatar': avatar, 'items': items})


@login_required
def create_avatar(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        avatar = Avatar.objects.create(user=user)  # Corrected to use the user instance
        # Assuming you want to redirect to a URL that uses the avatar's ID
        return redirect('dressup:dress_up', avatar_id=avatar.id)  # Corrected redirect
    return render(request, 'create_avatar.html')


@login_required
def purchase_item(request, item_id):
    item = Item.objects.get(id=item_id)
    PurchasedItem.objects.create(user=request.user, item=item)
    return redirect('dressup:mall')


@login_required
def mall(request):
    items = Item.objects.filter(premium=True)
    return render(request, 'mall.html', {'items': items})
