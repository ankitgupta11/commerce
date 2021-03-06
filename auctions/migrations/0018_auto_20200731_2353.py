# Generated by Django 3.0.8 on 2020-07-31 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20200731_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 31, 23, 53, 39, 155239)),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='listing',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(to='auctions.Listing'),
        ),
    ]
