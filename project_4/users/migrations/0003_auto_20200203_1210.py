# Generated by Django 2.1.7 on 2020-02-03 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_account_history_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='buyer_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='seller_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='account',
            name='winner_active',
            field=models.BooleanField(default=False),
        ),
    ]