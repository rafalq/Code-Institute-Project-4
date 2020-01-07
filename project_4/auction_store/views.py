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
from background_task import background


@background(schedule=30)
def test():
    return render(request, 'auction_store/home.html')


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
        form.instance.item = self.object
        form.instance.bidder = self.request.user
        form.save()
        return super(ItemDetailView, self).form_valid(form)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price', 'in_auction']

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    # @background(schedule=5)
    # def auction_sell(item_id):
    #     item = Item.objects.get(pk=item_id)
    #     item.update(sold=True)

    # auction_sell(item.id)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price', 'in_auction']

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
