# Generated by Django 2.1.7 on 2020-02-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='history_active',
            field=models.BooleanField(default=False),
        ),
    ]