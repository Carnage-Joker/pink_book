# utils.py

from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def get_default_user():
    ##function to get the default user
    return get_user_model().objects.get_or_create(username='defaultuser')[0]

# utils.py
def handle_error(request, message, redirect_url):
    from django.contrib import messages
    messages.error(request, message)
    return redirect(redirect_url)


# Example Usage in views.py


@login_required
def purchase_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.premium_only and not request.user.is_premium():
        return handle_error(request, "This item is for premium users only.", 'dressup:mall')
    # Additional logic...
