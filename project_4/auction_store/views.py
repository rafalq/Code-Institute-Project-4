from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import BidForm, CreateForm, OrderForm
from django.contrib.auth.models import User
from users.models import Account
from users.forms import AccountUpdateForm
from .models import Bid, Item, Order
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .filters import ItemFilter
from django.contrib.auth.decorators import login_required
import datetime
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET


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


@login_required
def payment(request, pk):  # new
    token = request.GET.get('stripeToken')
    item = Item.objects.get(pk=pk)
    order_form = OrderForm(request.POST)
    account = Account.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    context = {
        'item': item,
        'order_form': order_form,
        'account': account,
        'user': user
    }

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            charge = stripe.Charge.create(
                amount=int(item.price * 100),
                currency='eur',
                description=item.name,
                source=request.POST['stripeToken']
            )
            item.sold = True
            item.save()
            order_form.save()
            messages.success(request, f'You have bought!')
            return redirect('item-detail', item.id)
        else:
            messages.warning(request, f'Provide your delivery address!')
            order_form = OrderForm(request.POST)
    else:
        order_form = OrderForm(request.POST)

    return render(request, 'auction_store/payment.html', context)


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
        context['key'] = settings.STRIPE_PUBLISHABLE
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
            form.instance.end_date = timezone.now() + timezone.timedelta(minutes=2)
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
