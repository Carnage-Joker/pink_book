from .models import Avatar
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
    user = request.user
    avatar, created = Avatar.objects.get_or_create(user=user)
    if created:
        # Avatar was created
        return redirect('dressup:avatar_created')
    else:
        # Avatar already exists
        # Redirect to a different page if needed
        return redirect('dressup:avatar_exists')


def avatar_created(request):
    return render(request, 'avatar_created.html')


def avatar_exists(request):
    return render(request, 'avatar_exists.html')

@login_required
def purchase_item(request, item_id):
    item = Item.objects.get(id=item_id)
    PurchasedItem.objects.create(user=request.user, item=item)
    return redirect('dressup:mall')


@login_required
def mall(request):
    items = Item.objects.filter(premium=True)
    return render(request, 'mall.html', {'items': items})
