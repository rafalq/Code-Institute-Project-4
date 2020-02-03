# Generated by Django 2.1.7 on 2020-02-02 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='item_pics')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('price', models.IntegerField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('in_auction', models.BooleanField(default=False)),
                ('start_auction_price', models.IntegerField(blank=True, null=True)),
                ('sold', models.BooleanField(default=False)),
                ('sold_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sold_price', models.IntegerField(blank=True, null=True)),
                ('bought_at_auction', models.BooleanField(default=False)),
                ('test', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('MILITARY', 'Military'), ('PRIVATE', 'Private'), ('TOOLS', 'Tools'), ('TREASURE', 'Treasure'), ('WRITINGS', 'Writings'), ('OTHER', 'Other')], default='OTHER', max_length=20)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Cart')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(auto_now=True)),
                ('order_price', models.CharField(blank=True, max_length=40, null=True)),
                ('item_name', models.CharField(blank=True, max_length=100, null=True)),
                ('stripe_id', models.CharField(default='', max_length=40)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('street_address1', models.CharField(max_length=40)),
                ('street_address2', models.CharField(blank=True, max_length=40, null=True)),
                ('town_or_city', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=40)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction_store.Item'),
        ),
    ]
