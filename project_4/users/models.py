from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    owner = models.CharField(max_length=100, blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.owner}'s Cart"


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, blank=True, null=True)
    street_address1 = models.CharField(max_length=40, blank=True, null=True)
    street_address2 = models.CharField(max_length=40, blank=True, null=True)
    county = models.CharField(max_length=40, blank=True, null=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.SET_NULL, blank=True, null=True)
    history_active = models.BooleanField(default=False)
    history_checked = models.BooleanField(default=False)
    seller_active = models.BooleanField(default=False)
    buyer_active = models.BooleanField(default=False)
    winner_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Account'
