from django.urls import path
from . import views

app_name = 'virtual_try_on'

urlpatterns = [
    path('avatar_customization/', views.avatar_customization,
         name='avatar_customization'),
    path('update_avatar_feature/', views.update_avatar_feature,
         name='update_avatar_feature'),
    path('toggle_favorite_outfit/<int:pk>/',
         views.toggle_favorite_outfit, name='toggle_favorite_outfit'),
    path('favorites/', views.favorite_outfits_list, name='favorite_outfits_list'),
    path('my_avatar/', views.my_avatar, name='my_avatar'),
    path('outfits/', views.premium_outfit_list, name='premium_outfit_list'),
    path('dress_up_game/', views.dress_up_game, name='dress_up_game'),
    path('save_avatar/', views.save_avatar, name='save_avatar'),

    # other paths...
]
