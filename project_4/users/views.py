from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
from django.views.generic import ListView
from auction_store.models import Item, Bid


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
    template_name = 'users/storage.html'
    context_object_name = 'items'
    ordering = ['-start_date']

    def get_context_data(self, **kwargs):
        context = super(UserItemListView, self).get_context_data(**kwargs)
        context['bids'] = Bid.objects.all()
        return context


class UserBidListView(ListView):
    model = Bid
    template_name = 'users/storage.html'
    context_object_name = 'bids'
    ordering = ['-date']
