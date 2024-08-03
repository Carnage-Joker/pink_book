# In your new app's urls.py

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
]

