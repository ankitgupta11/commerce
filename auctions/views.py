from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Listing, ListingForm, Bid, BidForm, Category, Watchlist, Comment, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True),
        "count": Listing.objects.filter(active=True).count(),
        "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else ""
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listings(request):
    return HttpResponseRedirect(reverse("index"))

def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            listing.title = form.cleaned_data["title"]
            listing.description = form.cleaned_data["description"]
            listing.starting_bid = form.cleaned_data["starting_bid"]
            listing.created_at = datetime.now()
            listing.price = listing.starting_bid
            listing.image = form.cleaned_data["image"]
            listing.user = request.user
            if form.cleaned_data["category"]:
                listing.category = form.cleaned_data["category"]
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form,
                "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else ""
            })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": ListingForm,
            "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else ""
        })

def in_watchlist(user, listing):
    if user.is_authenticated == False:
        return False
    watchlist = user.watchlist.all()
    if watchlist:
        for w in watchlist:
            if listing == w.listing:
                return True
        else:
            return False
    else: False

def own_listing(user, listing):
    listing_user = listing.user
    if user == listing_user:
        return True
    else:
        return False

def listing(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
        if request.method == "POST":
            form = BidForm(request.POST, listing_id=listing_id)
            if form.is_valid():
                bid = Bid()
                bid.bid_amount = form.cleaned_data["bid_amount"]
                bid.user = request.user
                bid.listing = listing
                bid.save()
                listing.price = form.cleaned_data["bid_amount"]
                listing.save()
            else:
                return render(request, "auctions/listing.html", {
                    "bid_form": form,
                    "listing": listing,
                    "bid_count": listing.bids.all().count(),
                    "in_watchlist": in_watchlist(user=request.user, listing=listing),
                    "own_listing": own_listing(user=request.user, listing=listing),
                    "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else "",
                    "comments": listing.comments.order_by("-created_at"),
                    "comment_form": CommentForm,
                    "current_bid": listing.bids.last() and listing.bids.last().user == request.user
                })
    except Listing.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_count": listing.bids.all().count(),
        "bid_form": BidForm(listing_id=listing_id),
        "comment_form": CommentForm,
        "in_watchlist": in_watchlist(user=request.user, listing=listing),
        "own_listing": own_listing(user=request.user, listing=listing),
        "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else "",
        "comments": listing.comments.order_by("-created_at"),
        "current_bid": listing.bids.last() and listing.bids.last().user == request.user
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else ""
    })

def category(request, category_id):
    return render(request, "auctions/category.html", {
        "name": Category.objects.get(id=category_id),
        "listings": Listing.objects.filter(category=category_id, active=True),
        "count": Listing.objects.filter(category=category_id, active=True).count(),
        "watchlist_count": request.user.watchlist.all().count() if request.user.is_authenticated else ""
    })

def toggle_watchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=listing_id)
        if in_watchlist(user, listing):
            w=Watchlist.objects.get(user=user, listing=listing)
            w.delete()
        else:
            w=Watchlist()
            w.user = user
            w.listing = listing
            w.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    listing = []
    for i in watchlist:
        if i.listing.active == True:
            listing.append(i.listing)
    return render(request, "auctions/watchlist.html", {
        "listings": listing,
        "count": len(listing),
        "watchlist_count": request.user.watchlist.all().count()
    })

def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        if own_listing(request.user, listing):
            highest_bid = listing.bids.all().order_by('bid_amount').last()

            if highest_bid:
                highest_bidder = highest_bid.user
                listing.winner = highest_bidder

            listing.active = False
            listing.save()

            if in_watchlist(request.user, listing):
                w=Watchlist.objects.get(user=request.user, listing=listing)
                w.delete()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def post_comments(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.text = form.cleaned_data["text"]
            comment.user = request.user
            comment.listing = Listing.objects.get(id=listing_id)
            comment.created_at = datetime.now()
            comment.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))