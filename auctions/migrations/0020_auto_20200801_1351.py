# Generated by Django 3.0.8 on 2020-08-01 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_auto_20200801_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='winner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 1, 13, 51, 37, 964784)),
        ),
    ]
