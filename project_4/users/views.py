from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from auction_store.forms import BuyForm
from django.views.generic import ListView, UpdateView
from auction_store.models import Item, Bid
from django.db.models import OuterRef, Subquery


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AccountUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.account)
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
        'a_form': a_form
    }

    return render(request, 'users/profile.html', context)


class UserItemListView(ListView):
    model = Item
    template_name = 'users/history.html'
    context_object_name = 'items'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super(UserItemListView, self).get_context_data(**kwargs)
        context['bids'] = Bid.objects.all().order_by('-id')
        return context


class CartListView(ListView):
    model = Item
    template_name = 'users/cart.html'
    context_object_name = 'items'
    ordering = ['-end_date']

    def get_context_data(self, **kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)
        context['bids2'] = Bid.objects.all().order_by("-id")
        sq = Bid.objects.filter(item=OuterRef('item')).order_by(
            '-id')
        context['win_bids'] = Bid.objects.filter(bidder=self.request.user,
                                                 pk=Subquery(sq.values('pk')[:1]))
        return context

    @property
    def today_date(self):
        return timezone.now()
        # .isoformat()

    # def get_winner(self):
    #     if
    #     winner =


class ItemBuyUpdateView(LoginRequiredMixin, UpdateView):
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

# class CartDetailView(FormMixin, LoginRequiredMixin, SuccessMessageMixin, DetailView):
#     model = Item
#     form_class = BuyForm
#     success_message = "Buy!"

#     def get_success_url(self):
#         return reverse('cart', kwargs={'pk': self.object.id})

#     def get_context_data(self, **kwargs):
#         context = super(ItemDetailView, self).get_context_data(**kwargs)
#         context['bids'] = Bid.objects.filter(
#             item=self.object).order_by('-id')
#         context['form'] = BidForm(initial={'item': self.object})
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         bids = Bid.objects.filter(
#             item=self.object)
#         if self.object.end_date > form.instance.date:
#             if not bids and form.instance.amount > self.object.start_auction_price:
#                 form.instance.item = self.object
#                 form.instance.bidder = self.request.user
#                 form.save()
#             elif form.instance.amount > Bid.objects.last().amount:
#                 form.instance.item = self.object
#                 form.instance.bidder = self.request.user
#                 form.save()
#             else:
#                 return super(ItemDetailView, self).form_invalid(form)

#         return super(ItemDetailView, self).form_valid(form)

#     def get_absolute_url(self):
#         return reverse('item-detail', kwargs={'pk': self.pk})
