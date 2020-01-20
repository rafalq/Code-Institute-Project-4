from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import datetime


class Item(models.Model):
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True)
    in_auction = models.BooleanField(default=False)
    start_auction_price = models.IntegerField(null=True, blank=True)
    sold = models.BooleanField(default=False)
    bought_at_auction = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        User, null=True, related_name="buyer", on_delete=models.CASCADE)

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
    winner = models.ForeignKey(
        User, null=True, related_name="winner", on_delete=models.CASCADE)

    @property
    def today_date(self):
        return timezone.now()
