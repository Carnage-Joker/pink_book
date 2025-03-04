# utils.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def get_default_user():
    """
    Function to get the default user.
    """
    return get_user_model().objects.get_or_create(username='defaultuser')[0]

def handle_error(request, message, redirect_url):
    from django.contrib import messages
    messages.error(request, message)
    return redirect(redirect_url)


# Example Usage in views.py


@login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Item

def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, id=item_id)
    if item.premium_only and not request.user.is_premium():
        return handle_error(request, "This item is for premium users only.", 'dressup:mall')
    # Additional logic...
    return redirect('dressup:shop_detail', shop_id=item.shop.id)
