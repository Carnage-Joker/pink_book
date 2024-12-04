from django.urls import path
from . import views

app_name = 'dressup'

urlpatterns = [
    path('create-avatar/', views.create_avatar_view, name='create_avatar'),
    path('mall/', views.mall_view, name='mall'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('purchase/<int:item_id>/', views.purchase_item, name='purchase_item'),
    path('equip/<int:item_id>/', views.equip_item_view, name='equip_item'),
    
    # Add more URLs as needed
]
