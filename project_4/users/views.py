from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.models import User
from .models import Account
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, UpdateView, View
from auction_store.models import Item, Bid
from django.db.models import OuterRef, Subquery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    account = Account.objects.get(user=request.user)
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
        'a_form': a_form
    }

    return render(request, 'users/profile.html', context)


class UserItemListView(ListView):
    model = Item
    template_name = 'users/history.html'
    context_object_name = 'items'
    ordering = ['-start_date']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(UserItemListView, self).get_context_data(**kwargs)
        context['bids'] = Bid.objects.all().order_by('-id')
        return context


class CartListView(ListView):
    model = Item
    template_name = 'users/cart.html'
    context_object_name = 'items'
    ordering = ['-end_date']
    paginate_by = 2

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
