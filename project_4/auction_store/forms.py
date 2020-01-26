from django import forms
from .models import Bid, Item, Order


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']


# class BuyForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['sold']
#         widgets = {
#             'sold': forms.HiddenInput(),
#         }


class CreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['image', 'name', 'category', 'desc', 'price',
                  'in_auction', 'start_auction_price']


class OrderForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(OrderForm, self).__init__(*args, **kwargs)
    #     self.fields['full_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['phone_number'].required = True
    #     self.fields['street_address1'].required = True
    #     self.fields['town_or_city'].required = True
    #     self.fields['country'].required = True

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'street_address1',
                  'street_address2', 'town_or_city', 'country', 'postcode']
