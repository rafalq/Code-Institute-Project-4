from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    AccountUpdateForm,
    CartForm,
    LoginForm
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from .models import Account
from .filters import (
    SaleHistoryFilter,
    PurchaseHistoryFilter,
    BidHistoryFilter
)
from django.views.generic import ListView
from auction_store.models import Item, Bid
from users.models import Cart
from django.db.models import OuterRef, Subquery
import datetime


@property
def today_date(self):
    return timezone.now()


def register(request):
    items = Item.objects.all()
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        cart_form = CartForm()
        form = UserRegisterForm()

    context = {
        'form': form,
        'items': items
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    items = Item.objects.all()
    account = Account.objects.get(user=request.user)
    if account.history_active == False:
        account.history_checked = True
        account.save()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST, instance=request.user.account)
        if u_form.is_valid() and a_form.is_valid:
            u_form.save()
            a_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)

    # Update the cart
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
    context = {
        'u_form': u_form,
        'a_form': a_form,
        'items': items,
    }

    return render(request, 'users/profile.html', context)


def login_request(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('auction_store-store')
            else:
                messages.error(request, "Invalid username or password.")
                form = LoginForm(request=request, data=request.POST)

        else:
            messages.error(request, "Invalid username or password.")
            form = LoginForm(request=request, data=request.POST)
    context = {
        'form': form
    }
    return render(request, "users/login.html", context)


@login_required
def history(request):
    items = Item.objects.all().order_by('-id')
    bids = Bid.objects.all().order_by('-id')
    the_user = Account.objects.get(user=request.user)
    cart = Cart.objects.get(user=request.user)
    sale_filter = SaleHistoryFilter(request.GET, queryset=items)
    purchase_filter = PurchaseHistoryFilter(request.GET, queryset=items)
    bid_filter = BidHistoryFilter(request.GET, queryset=bids)

    for item in items:
        if item.finish_date != None:
            if (item.finish_date < item.today_date and
                    item.winner != None and item.cart == None):
                item.cart = cart
                the_user.cart = cart
                cart.total += 1
                the_user.history_active = False
                the_user.history_checked = True
                cart.save()
                the_user.save()
                item.save()

        if the_user.history_checked == True:
            the_user.seller_active = False
            the_user.buyer_active = False
            the_user.winner_active = False

    the_user.history_active = False
    the_user.save()

    if request.method == 'GET':
        the_user.history_checked = True
        the_user.save()

    context = {
        'items': items,
        'bids': bids,
        'the_user': the_user,
        'cart': cart,
        'sale_filter': sale_filter,
        'purchase_filter': purchase_filter,
        'bid_filter': bid_filter,
    }
    return render(request, 'users/history.html', context)


class CartListView(ListView):
    model = Item
    template_name = 'users/cart.html'
    context_object_name = 'items'
    ordering = ['-end_date']

    def get_context_data(self, *args, **kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)

        context['bids2'] = Bid.objects.all().order_by("-id")
        sq = Bid.objects.filter(item=OuterRef('item')).order_by(
            '-id')

        # find all latest bidders, if the auction finished, to get those who are users
        context['win_bids'] = Bid.objects.filter(bidder=self.request.user,
                                                 pk=Subquery(sq.values('pk')[:1]))

        # find won artifacts to update item's cart field
        # and the user's cart
        items = Item.objects.all()
        for item in items:
            # the auction is finished, there was at least 1 bidder
            if item.sold == False and item.finish_date != None:
                if (item.finish_date < item.today_date and
                        item.winner != None and item.cart == None):
                    # get the winner's cart
                    the_cart = Cart.objects.get(user=item.winner)
                    # assign the name of the winner's cart to the item's
                    item.cart = the_cart
                    item.save()
                    # add the won item amount to the cart's total
                    the_cart.total += 1
                    the_cart.save()

            # update the history as checked if the user has already seen it
            seller = Account.objects.get(user=item.seller)
            if seller.history_active == False:
                seller.history_checked = True
                seller.save()
        return context
