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

# class BuyForm(forms.ModelForm):

#     class Meta:
#         model = Item
#         exclude = ['image', 'desc', 'start_date',
#                    'in_auction', 'end_date', 'seller']
#         widgets = {
#             'sold': forms.HiddenInput,
#         }
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['email', 'first_name', 'last_name', 'birth_date']
#     email = forms.CharField(disabled=True)
