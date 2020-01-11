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
from .forms import BidForm, BuyForm
from .models import Bid, Item
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import datetime

# from .tasks import end_auction


def home(request):
    return render(request, 'auction_store/home.html')


class ItemListView(ListView):
    model = Item
    template_name = 'auction_store/store.html'
    context_object_name = 'items'
    ordering = ['-start_date']


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

    # @property
    # def today_date(self):
    #     return timezone.now()
    #     # .isoformat()

    # @property
    # def finish_date(self):
    #     return self.end_date
    #  # .isoformat()


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price',
              'in_auction', 'start_auction_price']

    def form_valid(self, form):
        if form.instance.in_auction and form.instance.start_auction_price == None:
            return super().form_invalid(form)
        else:
            form.instance.end_date = timezone.now() + timezone.timedelta(minutes=1)
            form.instance.seller = self.request.user
            return super().form_valid(form)


@property
def compare_dates(self):
    return datetime.now() > self.end_date


@property
def compare_d(self):
    return self.datetime.now() > self.end_date


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'name', 'desc', 'price']

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
    template_name = 'users/buy_form.html'

    def form_valid(self, form):
        item = self.get_object()
        if not item.sold:
            form.instance.sold = True
            form.instance.buyer = self.request.user
            return super().form_valid(form)

        return super(ItemBuyUpdateView, self).form_invalid(form)

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
