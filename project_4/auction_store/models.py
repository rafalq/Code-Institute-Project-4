from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import datetime


# def dtime():
#     return timezone.now() + timezone.timedelta(days=1)


class Item(models.Model):
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    start_date = models.DateTimeField(auto_now=True)
    in_auction = models.BooleanField(default=False)
    start_auction_price = models.IntegerField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sold = models.BooleanField(null=True)
    buyer = models.ForeignKey(
        User, null=True, related_name="buyer", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        if self.in_auction:
            self.end_date = timezone.now() + timezone.timedelta(days=1)
            super(Item, self).save(*args, **kwargs)
        else:
            super(Item, self).save(*args, **kwargs)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})

    @property
    def today_date(self):
        return timezone.now().isoformat()

    @property
    def finish_date(self):
        return self.end_date.isoformat()


class Bid(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
