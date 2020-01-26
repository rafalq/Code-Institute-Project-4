from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=40, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, blank=True, null=True)
    street_address1 = models.CharField(max_length=40, blank=True, null=True)
    street_address2 = models.CharField(max_length=40, blank=True, null=True)
    county = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Account'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
