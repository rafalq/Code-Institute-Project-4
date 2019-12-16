from django.shortcuts import render
from django.views.generic import ListView
from .models import Bid, Item


def home(request):
    return render(request, 'auction_store/home.html')


def store(request):
    all_items = {
        'items': Item.objects.all()
    }
    return render(request, 'auction_store/store.html', all_items)


def item(request):
    auction = {
        'bids': Bid.objects.all()
    }

    return render(request, 'auction_store/item.html', auction)


"""
class ItemListView(ListView):
    model = Item
    template_name = 'auction_store/store.html'
    all_items_object_name = 'items'
    ordering = ['-item_bid_start_date']
"""
