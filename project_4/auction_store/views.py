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
from django.contrib.messages.views import SuccessMessageMixin
from .forms import BidForm, BuyForm, CreateForm
from .models import Bid, Item
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .filters import ItemFilter
import datetime


def home(request):
    items_auction = Item.objects.filter(
        in_auction=True).order_by('id')

    context = {
        'items_auction': items_auction,
    }

    return render(request, 'auction_store/home.html', context)


def search(request):
    query = request.GET.get('q')
    results = Item.objects.filter(Q(
        name__icontains=query) | Q(
        category__icontains=query) | Q(
        desc__icontains=query) | Q(
        price__icontains=query) | Q(
        seller__username__icontains=query) | Q(
        buyer__username__icontains=query))
    context = {
        'results': results
    }
    messages.success(
        request, f'Found!')
    return render(request, 'auction_store/results.html', context)


class ItemListView(ListView):
    model = Item
    template_name = 'auction_store/store.html'
    context_object_name = 'items'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ItemFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class ItemDetailView(FormMixin, LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Item
    form_class = BidForm
    success_message = "Bid!"

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
        if self.object.end_date > form.instance.date:
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
    form_class = CreateForm
    success_url = '/store'
    success_message = 'You have just created ...!'
    template_name = 'auction_store/create_form.html'

    def form_valid(self, form):
        if form.instance.in_auction and form.instance.start_auction_price == None:
            return super(ItemCreateView, self).form_invalid(form)
        elif form.instance.in_auction and form.instance.start_auction_price is not None:
            form.instance.end_date = timezone.now() + timezone.timedelta(minutes=5)
            form.instance.seller = self.request.user
            return super().form_valid(form)
        else:
            form.instance.seller = self.request.user
            return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'name', 'category', 'desc', 'price']

    def form_valid(self, form):
        item = self.get_object()
        if not item.sold:
            form.instance.seller = self.request.user
            return super().form_valid(form)

        return super(ItemUpdateView, self).form_invalid(form)

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


class ItemBuyUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Item
    form_class = BuyForm
    success_url = '/store'
    success_message = 'You have just bought ...!'
    template_name = 'auction_store/buy_form.html'

    def form_valid(self, form):
        item = self.get_object()

        if not item.sold:
            form.instance.sold = True
            form.instance.buyer = self.request.user
            return super().form_valid(form)

        return super(ItemBuyUpdateView, self).form_invalid(form)
