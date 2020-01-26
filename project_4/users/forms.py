from django import forms
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['full_name', 'phone_number', 'country', 'postcode',
                  'town_or_city', 'street_address1', 'street_address2', 'county']
