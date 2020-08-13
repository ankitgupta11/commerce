from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm, Textarea, NumberInput
from datetime import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)   

    def __str__(self):
        return self.name 

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=datetime.now())
    image = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title 

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']

    def clean(self):
        cd = self.cleaned_data
        if cd.get('starting_bid') and cd.get('starting_bid') < 0:
            self.add_error('starting_bid', "This value can't be less than 0.")
        return cd

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.DecimalField(decimal_places=2, max_digits=10)

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        widgets = {
            'bid_amount': NumberInput(attrs={'placeholder': 'Bid'}),
        }

    def __init__(self, *args, **kwargs):
        self.listing_id = kwargs.pop('listing_id')
        super(BidForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        listing = Listing.objects.get(id=self.listing_id)
        if cd.get('bid_amount') or cd.get('bid_amount') == 0:
            if cd.get('bid_amount') < 0:
                self.add_error('bid_amount', "This value can't be less than 0.")
            elif cd.get('bid_amount') < listing.starting_bid:
                self.add_error('bid_amount', "Please raise your bid.")
            elif cd.get('bid_amount') <= listing.price and listing.bids.count() > 0:
                self.add_error('bid_amount', "Please raise your bid.")
        return cd

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'placeholder': 'Add a public comment...'}),
        }
