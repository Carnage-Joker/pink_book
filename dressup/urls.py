# In your new app's urls.py

from .views import (
    CreateAvatarView, DressUpView, PurchasePremiumOutfitView,
    FavoriteOutfitListView, PhotoshootLocationView
)
from django.urls import include, path
from django.urls import path
from . import views

app_name = 'dressup'

urlpatterns = [
    path('create_avatar/', views.create_avatar, name='create_avatar'),
    path('dress_up/', views.dress_up, name='dress_up'),
    path('purchase-item/<int:item_id>/',
         views.purchase_item, name='purchase_item'),
    path('mall/', views.mall, name='mall'),
    path('avatar_created/', views.avatar_created, name='avatar_created'),
    path('avatar_exists/', views.avatar_exists, name='avatar_exists'),
    path('create-avatar/', CreateAvatarView.as_view(), name='create_avatar'),
    path('my-avatar/', DressUpView.as_view(), name='my_avatar'),
    path('premium-outfit/<int:outfit_id>/purchase/',
         PurchasePremiumOutfitView.as_view(), name='purchase_premium_outfit'),
    path('favorite-outfits/', FavoriteOutfitListView.as_view(),
         name='favorite_outfit_list'),
    path('mall/', PhotoshootLocationView.as_view(), name='mall'),
]
