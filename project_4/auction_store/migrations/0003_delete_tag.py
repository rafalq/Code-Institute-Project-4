# Generated by Django 2.1.7 on 2020-01-15 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0002_remove_tag_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
