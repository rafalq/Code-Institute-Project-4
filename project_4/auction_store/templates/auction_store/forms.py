from django import forms
from django.contrib.auth.models import User
from .models import Bid


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['amount']
