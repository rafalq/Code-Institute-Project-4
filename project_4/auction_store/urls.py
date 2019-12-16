from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='auction_store-home'),
    path('store/', views.store, name='auction_store-store'),
    path('store/item/', views.item, name='auction_store-item')
]
