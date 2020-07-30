from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.IntegerField()
    duration = models.IntegerField()
    image = models.URLField(blank=True, null=True)

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'duration', 'image']
		
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_time = models.DateTimeField()
    bid_amount = models.IntegerField()

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        
'''
class Comment(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    time_sent = models.DateTimeField(default=timezone.now)
    '''