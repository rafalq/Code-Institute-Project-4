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
from django.views.generic.edit import FormMixin
from .forms import BidForm, BuyForm
from .models import Bid, Item
from django.urls import reverse
from django.contrib import messages
import datetime

# from .tasks import end_auction


def home(request):
    return render(request, 'auction_store/home.html')


class ItemListView(ListView):
    model = Item
    template_name = 'auction_store/store.html'
    context_object_name = 'items'
    ordering = ['-start_date']


class ItemDetailView(FormMixin, LoginRequiredMixin, DetailView):
    model = Item
    form_class = BidForm

    def get_success_url(self):
        return reverse('item-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['bids'] = Bid.objects.filter(
            item=self.object).order_by('-id')
        context['form'] = BidForm(initial={'item': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        bids = Bid.objects.filter(
            item=self.object)
        if not bids and form.instance.amount > self.object.start_auction_price:
            form.instance.item = self.object
            form.instance.bidder = self.request.user
            form.save()
        elif form.instance.amount > Bid.objects.last().amount:
            form.instance.item = self.object
            form.instance.bidder = self.request.user
            form.save()
        else:
            return super(ItemDetailView, self).form_invalid(form)

        return super(ItemDetailView, self).form_valid(form)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price',
              'in_auction', 'start_auction_price']

    def form_valid(self, form):
        if form.instance.in_auction and form.instance.start_auction_price == None:
            return super().form_invalid(form)
        else:
            form.instance.seller = self.request.user
            return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price']

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


class ItemBuyUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = BuyForm
    template_name = 'auction_store/buy_form.html'

    def form_valid(self, form):
        form.instance.sold = True
        form.instance.buyer = self.request.user
        return super().form_valid(form)

# class WinAuctionUpdateView(LoginRequiredMixin, UpdateView):
#     model = Item
#     form_class = BuyForm
#     template_name = 'auction_store/buy_form.html'

#     def form_valid(self, form):
#         form.instance.sold = True
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(ItemDetailView, self).get_context_data(**kwargs)
#         context['bids'] = Bid.objects.filter(
#             item=self.object).order_by('-id')
#         context['form'] = BidForm(initial={'item': self.object})
#         return context
