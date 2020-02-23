from django.urls import path
from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
)
from . import views

urlpatterns = [
    path('', views.home, name='auction_store-home'),
    path('store/', ItemListView.as_view(), name='auction_store-store'),
    path('store/new/', ItemCreateView.as_view(), name='item-create'),
    path('store/item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('store/item/<int:pk>/update/',
         ItemUpdateView.as_view(), name='item-update'),
    path('store/item/<int:pk>/delete/',
         ItemDeleteView.as_view(), name='item-delete'),
    path('store/item/<int:pk>/payment/', views.payment, name='payment'),
]
