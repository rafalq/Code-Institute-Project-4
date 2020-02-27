# Generated by Django 3.0.3 on 2020-02-27 19:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0013_auto_20200227_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='end_date',
            field=models.DateTimeField(blank=True, choices=[(datetime.datetime(2020, 2, 28, 19, 49, 46, 136520, tzinfo=utc), '24H'), (datetime.datetime(2020, 3, 2, 19, 49, 46, 136520, tzinfo=utc), '4 Days'), (datetime.datetime(2020, 3, 10, 19, 49, 46, 136520, tzinfo=utc), '12 days'), (datetime.datetime(2020, 3, 22, 19, 49, 46, 136520, tzinfo=utc), '24 Days')], null=True, verbose_name='Auction Period'),
        ),
    ]
