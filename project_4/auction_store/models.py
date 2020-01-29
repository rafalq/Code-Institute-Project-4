from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Account
from django.urls import reverse
from PIL import Image
import datetime


class Item(models.Model):
    image = models.ImageField(upload_to='item_pics', default='default.jpg')
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    in_auction = models.BooleanField(default=False)
    start_auction_price = models.IntegerField(null=True, blank=True)
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(default=timezone.now)
    sold_price = models.IntegerField(null=True, blank=True)
    bought_at_auction = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        User, null=True, related_name="buyer", on_delete=models.CASCADE)
    winner = models.ForeignKey(
        User, null=True, related_name="winner", on_delete=models.CASCADE)

    MILITARY = 'MILITARY'
    PRIVATE = 'PRIVATE'
    TOOLS = 'TOOLS'
    TREASURE = 'TREASURE'
    WRITINGS = 'WRITINGS'
    OTHER = 'OTHER'
    CATEGORY = [
        (MILITARY, 'Military'),
        (PRIVATE, 'Private'),
        (TOOLS, 'Tools'),
        (TREASURE, 'Treasure'),
        (WRITINGS, 'Writings'),
        (OTHER, 'Other'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY,
        default=OTHER,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    @property
    def today_date(self):
        return timezone.now()

    @property
    def finish_date(self):
        return self.end_date


class Bid(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def today_date(self):
        return timezone.now()


class Order(models.Model):
    order_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now=True)
    order_price = models.CharField(max_length=40, blank=True, null=True)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_buyer")
    item_name = models.CharField(max_length=100, blank=True, null=True)
    stripe_id = models.CharField(max_length=40, default='')
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=20)
    street_address1 = models.CharField(max_length=40)
    street_address2 = models.CharField(max_length=40, blank=True, null=True)
    town_or_city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.item_name)
