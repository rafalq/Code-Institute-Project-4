from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='auction_store-home'),
    path('search/', views.search, name='auction_store-search'),
    path('search/item/', views.item, name='auction_store-item')
]
