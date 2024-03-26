from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from .models import *
from .forms import ListingForm, Bidform


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        'title': "Listings",
        'listings' : listings
    })

def active(request):
    listings = [listing for listing in Listing.objects.all() if listing.is_active()]
    return render(request, "auctions/index.html",{
        'title': "Active listings",
        'listings' : listings
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
    
def listing(request, listing_id):
    try:
        bid_form = Bidform()
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        return Http404("Page Not Found")
    return render(request, 'auctions/listing.html', {
        'listing':listing,
        'form': bid_form,
        "title": listing.title
    })


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.owner = request.user
            model.save()
            # checking date
            return HttpResponseRedirect(reverse('index'))
    else:
        form = ListingForm()
        return render(request, 'auctions/create_listing.html', {
            'form': form,
            "title": "Create a listing"
        })
    
def bidding(request, listing_id):
    if request.method == 'POST':
        form = Bidform(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            listing = Listing.objects.get(pk=listing_id)
            
            current_bid = Bid.objects.filter(listing=listing)
            is_valid_bid = new_bid.amount >= listing.price
            is_highest = all(new_bid.amount > bid.amount for bid in current_bid)

            if is_valid_bid and is_highest:
                new_bid.user = request.user
                new_bid.listing = listing
                new_bid.highest_bidder = request.user
                new_bid.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        user_current_watchlist = request.user.watchlist.all()
        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            return Http404("ERROR PAGE NOT FOUND")
        
        if 'add' in request.POST:
            if listing in user_current_watchlist:
                messages.warning(request, "Can't add item that is already on your watchlist!")
            else:
                request.user.watchlist.add(listing)
                messages.success(request, "Added to watchlist successfully.")
        elif 'remove' in request.POST:
            if listing not in user_current_watchlist:
                messages.warning(request, "Can't remove item that is not on your watchlist!")
            else:
                request.user.watchlist.remove(listing)
                messages.error(request, "Removed from watchlist successfully.")
        else:
            return Http404("Error 404")
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


def watchlist(request):
    if not request.user.is_authenticated:
        raise Http404("ERROR YOU MUST LOG IN TO SEE WATCHLIST PAGE")
    else:
        listings = request.user.watchlist.all()
        return render(request, 'auctions/index.html', {
            "title": "Watchlist",
            "listings": listings
        })


def category(request):
    all_categories = Category.objects.all()
    return render(request, 'auctions/category.html', {
        "title": "Categories",
        "categories": all_categories
    })

def listing_by_category(request, category_name):
    listings = Listing.objects.select_related('category').filter(category__name = category_name)
    return render(request, 'auctions/index.html', {
        'title': "Categories",
        'listings': listings
    })