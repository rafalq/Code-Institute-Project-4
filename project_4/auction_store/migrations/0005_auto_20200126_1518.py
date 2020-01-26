# Generated by Django 2.1.7 on 2020-01-26 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0004_auto_20200126_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
