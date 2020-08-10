# Generated by Django 3.0.8 on 2020-07-31 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200731_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='starting_bid',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='bid_time',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='duration',
        ),
        migrations.AddField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 31, 21, 7, 52, 906888)),
        ),
    ]