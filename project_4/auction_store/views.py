from django.shortcuts import render
from .models import Bid


def home(request):
    return render(request, 'auction_store/home.html')


def search(request):
    return render(request, 'auction_store/search.html')


def item(request):
    auction = {
        'bids': Bid.objects.all()
    }

    return render(request, 'auction_store/item.html', auction, {'page_title': 'Item Name'})
