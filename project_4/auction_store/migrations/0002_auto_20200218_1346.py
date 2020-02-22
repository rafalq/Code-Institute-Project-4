# Generated by Django 2.1.7 on 2020-02-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Military', 'Military'), ('Private', 'Private'), ('Tools', 'Tools'), ('Treasure', 'Treasure'), ('Artistic', 'ARTISTIC'), ('Other', 'Other')], default='Other', max_length=20),
        ),
    ]