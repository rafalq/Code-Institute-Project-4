from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Bid(models.Model):
    bid_amount = models.IntegerField()
    bid_date = models.DateTimeField(default=timezone.now)
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE)

