# utils.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from .models import Item
from django.contrib.auth.models import AbstractBaseUser


def get_default_user():
    """
    Function to get the default user.
    """
    return get_user_model().objects.get_or_create(username='defaultuser')[0]


def handle_error(request: HttpRequest, message: str, redirect_url: str):
    sassy_error(request, message)
    return redirect(redirect_url)


# utils.py


def sassy_info(request: HttpRequest, message: str):
    """
    Adds an informational sassy pop-up message.
    """
    messages.add_message(request, messages.INFO, message,
                         extra_tags='sassy-popup')


def sassy_error(request: HttpRequest, message: str):
    """
    Adds an error sassy pop-up message.
    """
    messages.add_message(request, messages.ERROR, message,
                         extra_tags='sassy-popup')
    
def get_equipped_items(user: AbstractBaseUser) -> list:
    """
    Returns a list of equipped items for the user.
    Assumes the user model has a ManyToManyField to Item.
    """
    user = get_user_model().objects.get_or_create(username=user.sissy_name)[0]
    if not hasattr(user, 'equipped_items') or not callable(getattr(user.equipped_items, 'all', None)):
        raise AttributeError("User object does not have an 'equipped_items' attribute with an 'all()' method.")
    return user.equipped_items.all()


def add_clothing_to_favorites(user, item: Item) -> bool:
    """
    Adds a clothing item to the user's favorites.
    Assumes the user model has a 'favorites' ManyToManyField to Item.
    """
    user = get_user_model().objects.get_or_create(username=user.sissy_name)[0]
    if not hasattr(user, 'favorites') or not callable(getattr(user.favorites, 'all', None)):
        raise AttributeError("User object does not have a 'favorites' attribute with an 'all()' method.")
    if not user.is_authenticated:
        return False
    if item in user.favorites.all():
        return False
    user.favorites.add(item)
    return True    


def get_premium_items():
    return Item.objects.filter(is_premium=True)


def sassy_success(request, message):
    """
    Adds a success sassy pop-up message.
    """
    messages.add_message(request, messages.SUCCESS,
                         message, extra_tags='sassy-popup')

# Example Usage in views.py


@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, id=item_id)
    if item.premium_only and not request.user.is_premium():
        return handle_error(request, "This item is for premium users only.", 'dressup:mall')
    # Additional logic...
    return redirect('dressup:shop_detail', shop_id=item.shop.id)
