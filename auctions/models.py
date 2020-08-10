from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from datetime import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)   

    def __str__(self):
        return self.name 

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now())
    image = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title 

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
		
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    winner = models.BooleanField(default=False)
    bid_amount = models.PositiveIntegerField(error_messages={'required': 'Please enter your bid amount.'})

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
        
        
'''
class Comment(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now)
    '''