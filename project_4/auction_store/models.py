from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Item(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='items_pics')
    item_name = models.CharField(max_length=100)
    item_desc = models.TextField()
    item_price = models.IntegerField()
    item_bid_start_date = models.DateTimeField(auto_now=True)
    in_auction = models.BooleanField()
    item_bid_end_date = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class Bid(models.Model):
    bid_amount = models.IntegerField()
    bid_date = models.DateTimeField(default=timezone.now)
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE)
