# Generated by Django 3.0.8 on 2020-07-29 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
