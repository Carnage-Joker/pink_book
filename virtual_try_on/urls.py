# virtual_try_on/urls.py
from django.urls import path
from . import views

app_name = 'virtual_try_on'  # Define the namespace for this app

urlpatterns = [
    path('customize/', views.avatar_customization, name='avatar_customization'),
    path('update-avatar-feature/', views.update_avatar_feature,
         name='update_avatar_feature'),
    path('outfits/', views.premium_outfit_list, name='premium_outfit_list'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite_outfit,
         name='toggle_favorite_outfit'),
    path('favorites/', views.favorite_outfits_list, name='favorite_outfits_list'),
    path('my-avatar/', views.my_avatar, name='my_avatar'),
]

