from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


def dtime():
    return timezone.now() + timezone.timedelta(days=1)


# def dtime_prog_bar():
#     dtime_date = datetime.date(dtime)
#     tday = datetime.date.today()
#     till_day = dtime_date - tday
#     return(till_day.total_seconds())


class Item(models.Model):
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    start_date = models.DateTimeField(auto_now=True)
    in_auction = models.BooleanField()
    end_date = models.DateTimeField(default=dtime)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sold = models.BooleanField(null=True)
    buyer = models.ForeignKey(
        User, null=True, related_name="buyer", on_delete=models.CASCADE)

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        # if img.height > 300 or img.width > 300:
        #     output_size = (300, 300)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


class Bid(models.Model):
    amount = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(default=timezone.now)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
