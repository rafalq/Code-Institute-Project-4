from django import forms
from .models import Bid, Item, Order
from users.models import Cart


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


class CreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'name', 'category', 'desc', 'price',
                  'in_auction', 'start_auction_price', 'seller_active']
        widgets = {
            'seller_active': forms.HiddenInput(),
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'street_address1',
                  'street_address2', 'town_or_city', 'country', 'postcode',
                  'order_price', 'buyer', 'item_name', 'order_id']
        widgets = {
            'order_price': forms.HiddenInput(),
            'buyer': forms.HiddenInput(),
            'item_name': forms.HiddenInput(),
            'order_id': forms.HiddenInput(),
        }


# class CartUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Cart
#         fields = ['total']
