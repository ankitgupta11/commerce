# Generated by Django 3.0.8 on 2020-07-22 02:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('starting_bid', models.IntegerField()),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_time', models.DateTimeField()),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
