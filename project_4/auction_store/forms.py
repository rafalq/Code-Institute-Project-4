from django import forms
from .models import Bid, Item


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class BuyForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['sold']
        widgets = {
            'sold': forms.HiddenInput(),
        }


class CreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'name', 'category', 'desc', 'price',
                  'in_auction', 'start_auction_price']
