from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Account, Cart
from django.urls import reverse
from PIL import Image
import datetime


class Item(models.Model):
    image = models.ImageField(upload_to='item_pics', default='default.jpg')
    name = models.CharField(max_length=100)
    short = models.CharField(
        max_length=250, verbose_name="Short Description")
    origin_country = models.CharField(max_length=50)
    known_owners = models.CharField(
        max_length=150, verbose_name="Known Owners")
    desc = models.TextField(max_length=900, verbose_name="History")
    link_read_more = models.CharField(
        null=True, blank=True, max_length=900, verbose_name="Read More Link Address")
    price = models.IntegerField(verbose_name="Price (EURO)")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    in_auction = models.BooleanField(default=False)
    start_auction_price = models.IntegerField(
        null=True, blank=True, verbose_name="Auction Price (EURO)")
    sold = models.BooleanField(default=False)
    sold_date = models.DateTimeField(null=True, blank=True)
    sold_price = models.IntegerField(null=True, blank=True)
    bought_at_auction = models.BooleanField(default=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.ForeignKey(
        User, null=True, blank=True, related_name="buyer", on_delete=models.CASCADE)
    winner = models.ForeignKey(
        User, null=True, blank=True, related_name="winner", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL,
                             blank=True, null=True)
    seller_active = models.BooleanField(default=True)
    buyer_active = models.BooleanField(default=False)
    winner_active = models.BooleanField(default=False)

    MILITARY = 'Military'
    PRIVATE = 'Private'
    TOOLS = 'Tools'
    TREASURE = 'Treasure'
    ARTISTIC = 'Artistic'
    OTHER = 'Other'
    CATEGORY = [
        (MILITARY, 'Military'),
        (PRIVATE, 'Private'),
        (TOOLS, 'Tools'),
        (TREASURE, 'Treasure'),
        (ARTISTIC, 'Artistic'),
        (OTHER, 'Other'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY,
        default=OTHER,
    )

    VERY_BAD = 'Very Bad'
    BAD = 'Bad'
    OK = 'OK'
    GOOD = 'Good'
    VERY_GOOD = 'Very Good'
    PERFECT = 'Perfect'
    CONDITION = [
        (VERY_BAD, 'Very Bad'),
        (BAD, 'Bad'),
        (OK, 'OK'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very Good'),
        (PERFECT, 'Perfect'),
    ]
    condition = models.CharField(
        max_length=20,
        choices=CONDITION
    )

    # resizing images working only locally
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     image = Image.open(self.image.name)

    #     if image.height > 300 or image.width > 300:
    #         output_size = (300, 300)
    #         image.thumbnail(output_size)
    #         image.save(self.image.path)

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
    date = models.DateField(auto_now=True)
    order_price = models.CharField(max_length=40, blank=True, null=True)
    buyer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_buyer")
    item_name = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=50, verbose_name="Full Name*")
    email = models.EmailField(max_length=50, verbose_name="Email*")
    phone_number = models.CharField(
        max_length=20, verbose_name="Phone Number*")
    street_address1 = models.CharField(
        max_length=40, verbose_name="Street Address 1*")
    street_address2 = models.CharField(
        max_length=40, blank=True, null=True, verbose_name="Street Address 2")
    town_or_city = models.CharField(max_length=40, verbose_name="City*")
    county = models.CharField(
        max_length=40, blank=True, null=True, verbose_name="County")
    country = models.CharField(max_length=40, verbose_name="Country*")
    postcode = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Postcode")

    def __str__(self):
        return "{0} (id), {1} (order date), {2} (name)".format(self.id, self.date, self.item_name)
