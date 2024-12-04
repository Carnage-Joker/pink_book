# dressup/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Item, PurchasedItem, Shop
from django.contrib import messages
from .decorators import avatar_required

from .forms import AvatarCreationForm


from django.http import HttpRequest, HttpResponse


# dressup/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from .models import Avatar, Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required


# dressup/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from .models import Avatar, Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required


# dressup/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from .models import Avatar, Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required


# dressup/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from .models import Avatar, Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required


# dressup/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from .models import Avatar, Shop, Item, PurchasedItem
from .forms import AvatarCreationForm
from .decorators import avatar_required  # Ensure this decorator exists


@login_required
def create_avatar_view(request: HttpRequest) -> HttpResponse:
    """
    View to handle the creation of a new Avatar for the logged-in user.
    Simplified to only allow selection of skin tone and body type.
    Sets default values for other attributes.
    Redirects to the mall after creation.
    """
    # Check if the user already has an avatar
    if hasattr(request.user, 'avatar'):
        messages.info(
            request, "You already have an avatar. Redirecting to the mall.")
        return redirect('dressup:mall')

    if request.method == 'POST':
        form = AvatarCreationForm(request.POST)
        if form.is_valid():
            # Create the avatar without saving to assign the user and set defaults
            avatar = form.save(commit=False)
            avatar.user = request.user
            # Set default values
            avatar.hair = '00'  # Default hair choice
            avatar.hair_color = '00'  # Default hair color
            avatar.shoes = '00'  # Default shoes
            avatar.accessories = '00'  # Default accessories
            avatar.skirt = '00'  # Default skirt
            avatar.top = '00'  # Default top
            # Set a default name or allow user input
            avatar.name = f"{request.user.sissy_name}'s Avatar"
            avatar.save()
            messages.success(
                request, "Your avatar has been created successfully!")
            return redirect('dressup:mall')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AvatarCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'dressup/create_avatar.html', context)

@login_required
def purchase_item(request: HttpRequest, item_id: int) -> HttpResponse:
    item = get_object_or_404(Item, id=item_id)
    user = request.user  # type: User

    # Check if item is premium and user is not a premium subscriber
    if item.premium_only and not user.is_premium():  # type: ignore
        messages.error(
            request, "This item is available for premium subscribers only.")
        return redirect('shop')

    # Check if user has enough points or if the item requires real money
    if item.price_points and user.points >= item.price_points:
        user.deduct_points(item.price_points)  # type: ignore
        PurchasedItem.objects.create(user=user, item=item)
        messages.success(request, f"You have purchased {item.name}!")
        return redirect('inventory')
    elif item.price_dollars:
        # Redirect to payment processing
        pass  # Implement payment gateway logic here
    else:
        messages.error(
            request, "You do not have enough points to purchase this item.")
        return redirect('dressup:shop')

# dressup/views.py


# dressup/views.py

@login_required
@avatar_required
def equip_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    View to equip a purchased item to the user's avatar.
    """
    item = get_object_or_404(Item, id=item_id)
    avatar = request.user.avatar

    # Check if the item is purchased
    purchased = PurchasedItem.objects.filter(avatar=avatar, item=item).first()
    if not purchased:
        messages.error(request, "You have not purchased this item.")
        return redirect('dressup:mall')

    # Equip the item based on its category
    category = item.category  # Ensure 'category' field exists in Item model

    if category == 'hair':
        avatar.hair = item.value  # 'value' corresponds to hair choices
    elif category == 'hair_color':
        avatar.hair_color = item.value
    elif category == 'shoes':
        avatar.shoes = item.value
    elif category == 'accessories':
        avatar.accessories = item.value
    elif category == 'skirt':
        avatar.skirt = item.value
    elif category == 'top':
        avatar.top = item.value
    # Add more categories as needed

    avatar.save()
    messages.success(request, f"You have equipped {item.name} to your avatar.")
    return redirect('dressup:mall')


# dressup/views.py

@login_required
@avatar_required
def mall_view(request: HttpRequest) -> HttpResponse:
    """
    View to display the mall where users can upgrade their avatars.
    """
    shops = Shop.objects.all()
    avatar = request.user.avatar
    image_urls = avatar.get_image_urls()
    context = {
        'shops': shops,
        'avatar': avatar,
        'image_urls': image_urls,
    }
    return render(request, 'dressup/mall.html', context)


@login_required
def shop_detail(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    items = shop.items.all()
    context = {
        'shop': shop,
        'items': items,
    }
    return render(request, 'dressup/shop_detail.html', context)


@login_required
def inventory_view(request):
    purchased_items = PurchasedItem.objects.filter(user=request.user)
    context = {
        'purchased_items': purchased_items,
    }
    return render(request, 'dressup/inventory.html', context)
