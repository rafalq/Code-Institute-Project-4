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
    items_auction = Item.objects.filter(
        in_auction=True).order_by('id')
    items = Item.objects.all()

    # if the history was checked
    if request.user.is_authenticated:
        user = request.user
        if user.account.history_active == False:
            user.account.history_checked = True
            user.account.save()

    context = {
        'items_auction': items_auction,
        'items': items,
    }
    return render(request, 'auction_store/home.html', context)


def search(request):
    query = request.GET.get('q')
    items = Item.objects.filter(Q(
        name__icontains=query) | Q(
        category__icontains=query) | Q(
        desc__icontains=query) | Q(
        price__icontains=query) | Q(
        seller__username__icontains=query) | Q(
        buyer__username__icontains=query))

    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'items': items,
        'page_obj': page_obj
    }
    return render(request, 'auction_store/results.html', context)


@login_required
def payment(request, pk):
    if request.user.is_authenticated:
        winner = request.user
        # check if the auction is finish
        won_artifacts = Item.objects.filter(
            sold=False, end_date__lte=datetime.date.today())
        for art in won_artifacts:
            # if the winner is user
            if art.winner == request.user:
                cart = True
                break
            else:
                cart = False

    token = request.GET.get('stripeToken')
    item = Item.objects.get(pk=pk)
    bid = Bid.objects.filter(bidder=item.winner).last()
    order_form = OrderForm(request.POST)
    account = Account.objects.get(user=request.user)
    user = User.objects.get(id=request.user.id)

    # assign the price
    if item.in_auction:
        if timezone.now() > item.finish_date:
            if item.winner == None:
                price = item.price
                item.bought_at_auction = True
            else:
                price = bid.amount
        else:
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

            order_form.instance.order_price = price
            order_form.instance.buyer = request.user
            order_form.instance.order_id = item.id
            order_form.instance.item_name = item.name
            order_form.save()

            item.sold = True
            item.sold_price = price
            item.sold_date = timezone.now()
            item.buyer = request.user
            item.save()

            the_user = Account.objects.get(user=request.user)
            the_cart = Cart.objects.get(owner=request.user)
            the_cart.total -= 1
            the_user.history_active = True
            the_user.history_checked = False
            the_user.buyer_active = True
            # if the_cart.total == 0:
            #     the_cart = None
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
# displays all available items for sale / search option


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
        # place the won artifacts in the cart if the auction is over
        # update the users histories

        items = Item.objects.all()
        for item in items:
            # check if the artifact is at auction
            if item.finish_date != None:
                # check: 1. the auction is finish?
                       # 2. there is at least 1 bidder?
                       # 3. was it not in the cart already?
                if (item.finish_date < item.today_date and
                        item.winner != None and item.cart == None):
                    # if the above are true - update the cart
                    the_cart = Cart.objects.get(owner=item.winner)
                    winner = Account.objects.get(user=item.winner)
                    item.cart = the_cart
                    winner.cart = the_cart
                    # add the item to the cart's amount
                    the_cart.total += 1
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
                # let know the bidder about the new highest bid
                # if item.winner_active:
                #     if item.winner != None:
                #         winner = Account.objects.get(user=item.winner)
                #         winner.history_active = True
                #         winner.winner_active = True
                #         winner.save()

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
        context['key'] = settings.STRIPE_PUBLISHABLE
        context['orders'] = Order.objects.filter(order_id=self.object.id)

        if self.object.winner == None:
            context['sold_price'] = self.object.price
        else:
            bid = Bid.objects.filter(
                item=self.object).last()
            context['sold_price'] = bid.amount

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
    success_message = 'Well Done!'
    template_name = 'auction_store/create_form.html'

    def form_valid(self, form):
        if form.instance.in_auction and form.instance.start_auction_price == None:
            return super(ItemCreateView, self).form_invalid(form)
        elif form.instance.in_auction and form.instance.start_auction_price is not None:
            form.instance.end_date = timezone.now() + timezone.timedelta(minutes=30)
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
