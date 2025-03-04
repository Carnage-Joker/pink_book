from django.urls import path
from . import views

app_name = 'dressup'

urlpatterns = [
    path('create-avatar/', views.create_avatar_view, name='create_avatar'),
    path('mall/', views.mall_view, name='mall'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('equip/<int:item_id>/', views.equip_item_ajax, name='equip_item'),
    path('story_intro/', views.story_intro_view, name='story_intro'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('dress-up/', views.dress_up_view, name='dress_up'),
    # Add more URLs as needed
]
