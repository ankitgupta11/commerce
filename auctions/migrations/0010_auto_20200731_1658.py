# Generated by Django 3.0.8 on 2020-07-31 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200730_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.PositiveIntegerField(),
        ),
    ]
