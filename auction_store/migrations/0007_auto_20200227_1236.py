# Generated by Django 3.0.3 on 2020-02-27 12:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0006_auto_20200227_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='end_date',
            field=models.DateTimeField(blank=True, choices=[(datetime.datetime(2020, 2, 28, 12, 36, 58, 988284, tzinfo=utc), '24H'), (datetime.datetime(2020, 3, 1, 12, 36, 58, 988284, tzinfo=utc), '3 Days'), (datetime.datetime(2020, 3, 5, 12, 36, 58, 988284, tzinfo=utc), '1 Week'), (datetime.datetime(2020, 3, 19, 12, 36, 58, 988284, tzinfo=utc), '3 Weeks')], null=True),
        ),
    ]
