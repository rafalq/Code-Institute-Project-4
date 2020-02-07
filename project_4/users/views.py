from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    AccountUpdateForm,
    CartForm,
    LoginForm,
    CartUpdateForm
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

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        cart_form = CartForm(request.POST)
        if form.is_valid() and cart_form.is_valid():
            form.save()
            cart_form.instance.id = form.instance.id
            cart_form.instance.total = 0
            username = form.cleaned_data.get('username')
            cart_form.instance.owner = form.instance.username
            cart_form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        cart_form = CartForm(request.POST)
        form = UserRegisterForm()

    context = {
        'form': form,
        'cart_form': cart_form,
        'items': items
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    items = Item.objects.all()
    account = Account.objects.get(user=request.user)
    if account.history_active == False:
        account.history_checked = True
        # account.seller_active = False
        # account.buyer_active = False
        # account.winner_active = False
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
                # Update the Cart
                the_user = Account.objects.get(user=request.user)
                won_artifacts = Item.objects.filter(
                    winner=request.user, sold=False)
                the_cart = Cart.objects.get(owner=the_user.user.username)
                the_cart.total = 0
                the_user.cart = None
                for item in won_artifacts:
                    if item.end_date < item.today_date:
                        the_cart.total += 1
                        item.cart = the_cart
                        if the_cart.total > 0:
                            the_user.cart = the_cart
                        else:
                            the_user.cart = None
                    item.save()

                the_user.save()
                the_cart.save()
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
    cart = Cart.objects.get(owner=request.user)
    sale_filter = SaleHistoryFilter(request.GET, queryset=items)
    purchase_filter = PurchaseHistoryFilter(request.GET, queryset=items)
    bid_filter = BidHistoryFilter(request.GET, queryset=bids)
    # bid_items = Item.objects.filter(bid__bidder=request.user).distinct()
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
    # if request.method == 'POST' and 'btnitem' in request.POST:
    #     item_filter
    # if request.method == 'POST' and 'btnbid' in request.POST:
    #     bid_filter

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
        context['win_bids'] = Bid.objects.filter(bidder=self.request.user,
                                                 pk=Subquery(sq.values('pk')[:1]))
        items = Item.objects.all()
        for item in items:
            if item.finish_date != None:
                if (item.finish_date < item.today_date and
                        item.winner != None and item.cart == None):
                    the_cart = Cart.objects.get(owner=item.winner)
                    winner = Account.objects.get(user=item.winner)
                    item.cart = the_cart
                    winner.cart = the_cart
                    the_cart.total += 1
                    the_cart.save()
                    winner.save()
                    item.save()
            seller = Account.objects.get(user=item.seller)
            if seller.history_active == False:
                seller.history_checked = True
                seller.save()
        return context

# @login_required
# def history(request):
#     bids = Bid.objects.all().order_by('-id')
#     items = Item.objects.all().order_by('-id')
#     the_user = Account.objects.get(user=request.user)
#     cart = Cart.objects.get(owner=request.user)
#     for item in items:
#         if item.finish_date != None:
#             if (item.finish_date < item.today_date and
#                     item.winner != None and item.cart == None):
#                 item.cart = cart
#                 the_user.cart = cart
#                 cart.total += 1
#                 the_user.history_active = False
#                 the_user.history_checked = True
#                 cart.save()
#                 the_user.save()
#                 item.save()

#         if the_user.history_checked == True:
#             the_user.seller_active = False
#             the_user.buyer_active = False
#             the_user.winner_active = False

#     the_user.history_active = False
#     the_user.save()

#     context = {
#         'items': items,
#         'bids': bids,
#         'the_user': the_user,
#         'cart': cart
#     }
#     return render(request, 'users/history.html', context)


# class HistoryListView(ListView, LoginRequiredMixin):
#     model = Bid
#     template_name = 'users/history.html'
#     context_object_name = 'bids'
#     filterset_class = BidFilter
#     # paginate_by = 5

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = self.filterset_class(
#             self.request.GET, queryset=queryset)
#         return self.filterset.qs.distinct()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset

#         return context
        # UPDATE THE CART AND HISTORY
        # place the won artifacts in the cart if the auction is over
        # update the users histories

        # items = Item.objects.all()
        # for item in items:
        #     # check if the artifact is at auction
        #     if item.finish_date != None:
        #         # check: 1. the auction is finish?
        #                # 2. there is at least 1 bidder?
        #                # 3. was it not in the cart already?
        #         if (item.finish_date < item.today_date and
        #                 item.winner != None and item.cart == None):
        #             # if the above are true - update the cart
        #             the_cart = Cart.objects.get(owner=item.winner)
        #             winner = Account.objects.get(user=item.winner)
        #             item.cart = the_cart
        #             winner.cart = the_cart
        #             # add the item to the cart's amount
        #             the_cart.total += 1
        #             # update the user's history
        #             winner.winner_active = True
        #             the_cart.save()
        #             winner.save()
        #             item.save()
        #     # update the seller's history if the item has just been put in sale
        #     seller = Account.objects.get(user=item.seller)
        #     if item.seller_active:
        #         seller.history_active = True
        #         seller.history_checked = False
        #         seller.seller_active = True
        #         # update the item status
        #         item.seller_active = False

        #     else:
        #         # has the history been checked yet?
        #         if seller.history_active == False:
        #             seller.history_checked = True
        #     seller.save()
        #     item.save()

        #     if item.buyer != None:
        #          # if the item has just been bought?
        #         if item.buyer_active:
        #             buyer = Account.objects.get(user=item.buyer)
        #             # let know the buyer about their fresh purchase
        #             # by updating the buyer status
        #             # in the navbar
        #             buyer.history_active = True
        #             buyer.history_checked = False
        #             # and their own history
        #             buyer.buyer_active = True
        #             buyer.save()
        #             # update only once
        #             item.buyer_active = False
        #             item.save()
        #         # let know the bidder about the new highest bid
        #         # if item.winner_active:
        #         #     if item.winner != None:
        #         #         winner = Account.objects.get(user=item.winner)
        #         #         winner.history_active = True
        #         #         winner.winner_active = True
        #         #         winner.save()
