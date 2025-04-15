# utils.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from .models import Item


def get_default_user():
    """
    Function to get the default user.
    """
    return get_user_model().objects.get_or_create(username='defaultuser')[0]


def handle_error(request, message, redirect_url):
    sassy_error(request, message)
    return redirect(redirect_url)


# utils.py


def sassy_info(request, message):
    """
    Adds an informational sassy pop-up message.
    """
    messages.add_message(request, messages.INFO, message,
                         extra_tags='sassy-popup')


def sassy_error(request, message):
    """
    Adds an error sassy pop-up message.
    """
    messages.add_message(request, messages.ERROR, message,
                         extra_tags='sassy-popup')


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
