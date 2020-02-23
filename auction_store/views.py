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
from .models import Bid, Item, Order, Cart
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .filters import ItemFilter
from django.contrib.auth.decorators import login_required
import datetime
from django.conf import settings
import stripe
from django.core.paginator import Paginator


stripe.api_key = settings.STRIPE_SECRET


def home(request):
    # Update the cart
    items = Item.objects.all()
    for item in items:
        # check if the artifact is at auction
        if item.finish_date != None:
            # check: 1. the auction is finish?
                   # 2. there is at least 1 bidder?
                   # 3. has it not been in the cart yet?
            if (item.finish_date < item.today_date and
                    item.winner != None and item.cart == None):
                # if the above are true - update the cart
                the_cart = Cart.objects.get(user=item.winner)
                item.cart = the_cart
                # add the item to the cart's items amount
                the_cart.total += 1
                winner = Account.objects.get(user=item.winner)
                # update the user's history
                winner.winner_active = True
                the_cart.save()
                winner.save()
                item.save()
    # Update the history anytime the user is logged in
    if request.user.is_authenticated:
        user = request.user
        if user.account.history_active == False:
            user.account.history_checked = True
            user.account.save()
    return render(request, 'auction_store/home.html')


@login_required
def payment(request, pk):
    # Update the cart
    items = Item.objects.all()
    for item in items:
        # check if the artifact is at auction
        if item.finish_date != None:
            # check: 1. the auction is finish?
                   # 2. is there at least 1 bidder?
                   # 3. has it not been in a cart yet?
            if (item.finish_date < item.today_date and
                    item.winner != None and item.cart == None):
                # if the above are true - update the item's field cart
                the_cart = Cart.objects.get(user=item.winner)
                item.cart = the_cart
                # add the item to the cart's items amount
                the_cart.total += 1
                winner = Account.objects.get(user=item.winner)
                # update the user's history
                winner.winner_active = True
                the_cart.save()
                winner.save()
                item.save()
    if request.user.is_authenticated:
        winner = request.user
        # find items whose auctions are finish
        # and those that weren't bought during the auction
        won_artifacts = Item.objects.filter(
            sold=False, end_date__lte=datetime.date.today())

    token = request.GET.get('stripeToken')
    item = Item.objects.get(pk=pk)
    # find the latest bid for assigning the price
    bid = Bid.objects.filter(bidder=item.winner).last()
    order_form = OrderForm(request.POST)
    account = Account.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)
    order_form = OrderForm(instance=request.user.account)
    # assign the price
    if item.in_auction:
        # the auction finished but no bidder
        if timezone.now() > item.finish_date:
            if item.winner == None:
                price = item.price
                item.bought_at_auction = True
            else:
                # the auction finished, at least 1 bidder
                price = bid.amount
        else:
            # the auction not finished, item will be bought for the sale price
            price = item.price
            item.bought_at_auction = True
    else:
        price = item.price

    context = {
        'item': item,
        'order_form': order_form,
        'account': account,
        'user': user,
        'price': price
    }

    if request.method == 'POST' and not item.sold:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            charge = stripe.Charge.create(
                amount=int(price * 100),
                currency='eur',
                description=item.name,
                source=request.POST['stripeToken']
            )
            # create the order object
            order_form.instance.order_price = price
            order_form.instance.buyer = request.user
            order_form.instance.order_id = item.id
            order_form.instance.item_name = item.name
            order_form.save()
            # update the item's fields connecting to the purchase
            item.sold = True
            item.sold_price = price
            item.sold_date = timezone.now()
            item.buyer = request.user
            item.save()
            # update the user's cart
            the_cart = Cart.objects.get(user=request.user)
            the_cart.total -= 1
            # update the user's history
            the_user = Account.objects.get(user=request.user)
            the_user.history_active = True
            the_user.history_checked = False
            the_user.buyer_active = True
            the_user.save()
            the_cart.save()

            messages.success(request, f'Your order was successful!')
            return redirect('item-detail', item.id)
        else:
            messages.warning(
                request, f'Invalid data received!')
            order_form = OrderForm(request.POST)
    else:
        order_form = OrderForm(request.POST)

    return render(request, 'auction_store/payment.html', context)


# STORE
# displays all available items for sale
# search option

class ItemListView(ListView, LoginRequiredMixin):
    model = Item
    template_name = 'auction_store/store.html'
    context_object_name = 'items'
    filterset_class = ItemFilter
    ordering = ['-start_date']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(
            self.request.GET, queryset=queryset)

        # UPDATE THE CART AND HISTORY
        # place all won artifacts in the cart if the auction is over
        # update the users histories

        items = Item.objects.all()
        for item in items:
            # check if the artifact is at auction
            if item.in_auction:
                # check: 1. the auction is finish?
                       # 2. is there at least 1 bidder?
                       # 3. has it not been in the cart yet?
                if (item.finish_date < item.today_date and
                        item.winner != None and item.cart == None):
                    # if the above are true - update the cart
                    the_cart = Cart.objects.get(user=item.winner)
                    item.cart = the_cart
                    # add the item to the cart's items amount
                    the_cart.total += 1
                    winner = Account.objects.get(user=item.winner)
                    # update the user's history
                    winner.winner_active = True
                    the_cart.save()
                    winner.save()
                    item.save()

            # update the seller's history if the item has just been put in sale
            seller = Account.objects.get(user=item.seller)
            if item.seller_active:
                seller.history_active = True
                seller.history_checked = False
                seller.seller_active = True
                # update the item status
                item.seller_active = False

            else:
                # has the history been checked yet?
                if seller.history_active == False:
                    seller.history_checked = True
            seller.save()
            item.save()

            if item.buyer != None:
                 # if the item has just been bought?
                if item.buyer_active:
                    buyer = Account.objects.get(user=item.buyer)
                    # let know the buyer about their fresh purchase
                    # by updating the buyer status
                    # in the navbar
                    buyer.history_active = True
                    buyer.history_checked = False
                    # and their own history
                    buyer.buyer_active = True
                    buyer.save()
                    # update only once
                    item.buyer_active = False
                    item.save()

        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

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

        if self.object.winner == None:
            context['sold_price'] = self.object.price
        else:
            bid = Bid.objects.filter(
                item=self.object).last()
            context['sold_price'] = bid.amount

        # Update the cart
        items = Item.objects.all()
        for item in items:
            # check if the artifact is at auction
            if item.finish_date != None:
                # check: 1. the auction is finish?
                       # 2. is there at least 1 bidder?
                       # 3. has it not been in the cart yet?
                if (item.finish_date < item.today_date and
                        item.winner != None and item.cart == None):
                    # if the above are true - update the cart
                    the_cart = Cart.objects.get(user=item.winner)
                    item.cart = the_cart
                    # add the item to the cart's items amount
                    the_cart.total += 1
                    winner = Account.objects.get(user=item.winner)
                    # update the user's history
                    winner.winner_active = True
                    the_cart.save()
                    winner.save()
                    item.save()
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
        the_bidder = self.request.user
        if self.object.end_date > form.instance.date:
            if not bids and form.instance.amount > self.object.start_auction_price:
                form.instance.item = self.object
                form.instance.bidder = self.request.user
                self.object.winner = self.request.user
                the_bidder.account.winner_active = True
                the_bidder.account.history_active = True
                the_bidder.account.history_checked = False
                the_bidder.account.save()
                self.object.save()
                form.save()
            elif form.instance.amount > Bid.objects.last().amount:
                form.instance.item = self.object
                form.instance.bidder = self.request.user
                self.object.winner = self.request.user
                the_bidder.account.winner_active = True
                the_bidder.account.history_active = True
                the_bidder.account.history_checked = False
                the_bidder.account.save()
                self.object.save()
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
    template_name = 'auction_store/create_form.html'

    def form_valid(self, form):
        if form.instance.start_auction_price is not None:
            form.instance.in_auction = True
            form.instance.end_date = timezone.now() + timezone.timedelta(days=24)
            form.instance.seller = self.request.user
            return super().form_valid(form)
        else:
            form.instance.seller = self.request.user
            return super().form_valid(form)


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['image', 'name', 'category',
              'price', 'short', 'condition',
              'origin_country', 'known_owners', 'desc', 'link_read_more']

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
