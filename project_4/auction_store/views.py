from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Bid, Item


def home(request):
    return render(request, 'auction_store/home.html')


def store(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'auction_store/store.html', context)


def item(request):
    context = {
        'bids': Bid.objects.all()
    }

    return render(request, 'auction_store/item.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'auction_store/store.html'
    context_object_name = 'items'
    ordering = ['-item_bid_start_date']


class ItemDetailView(DetailView):
    model = Item


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['image', 'item_name', 'item_desc', 'item_price', 'in_auction']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'item_name', 'item_desc', 'item_price', 'in_auction']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.seller:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.seller:
            return True
        return False
