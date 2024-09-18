from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListingForm, BidForm


# USER: tatooine
# PASSWORD : alvaro
def index(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html",
                      {"listings": Listing.objects.all().filter(active=True),
                       "watchlist": request.user.watchlist.all()})
    else:
        return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html",
                      {"categories": Listing.Category.choices,
                       "listings": Listing.objects.all(),
                       "selected_category": None})
    if request.method == "POST":
        selected_category = request.POST["category"]
        print("Selected Category: ", selected_category)
        filtered_listings = Listing.objects.filter(category=selected_category)
        print("Filtered_listings: ", filtered_listings)
        print("All: ", Listing.objects.all())
        return render(request, "auctions/categories.html",
                      {"categories": Listing.Category.choices,
                       "listings": filtered_listings,
                       "selected_category": selected_category})



def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        listing = get_object_or_404(Listing, pk=listing_id)

        if listing not in request.user.watchlist.all():
            print(request.user.watchlist.all())
            print("Listing added successfully")
            request.user.watchlist.add(listing)
        else:
            print("Listing already added")
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist": request.user.watchlist.all(),
        })


def remove_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("auctions:index"))

def create_listing(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST)
        print("Listing Form: ", listing_form)

        if listing_form.is_valid():
            listing_cleaned = listing_form.cleaned_data
            print("Listing_cleaned: ", listing_cleaned)
            l = Listing(author=request.user,
                        title=listing_cleaned["title"],
                        description=listing_cleaned["description"],
                        price=listing_cleaned["price"],
                        category=listing_cleaned["category"],
                        image=listing_cleaned["image"],
                        )
            l.save()
            print("printing l: ", l)  # if not __str__, django prints by default the id(after saving)

            return HttpResponseRedirect(reverse("auctions:listings", args=[l.id]))
    else:
        listing_form = ListingForm()

    return render(request, "auctions/create_listing.html", {
        "listing_form": listing_form,
    })

#TODO sort listing, price more digits.

@login_required
def listings(request, listing_id):
    # listing = Listing.objects.get(pk=listing_id)
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "GET":
        f = BidForm(listing=listing)
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "form": f,
            "user": request.user
        })

    elif request.method == "POST":
        f= BidForm(request.POST, listing=listing)
        if f.is_valid():
            bid_amount = f.cleaned_data["place_bid"]

            current_bid = listing.current_bid
            min_bid = listing.price if current_bid is None else current_bid.bid

            if bid_amount > min_bid:
                new_bid = Bid(auction=listing, bid=bid_amount, author=request.user)
                new_bid.save()

                listing.current_bid = new_bid
                listing.n_bids += 1
                listing.save()

            return HttpResponseRedirect(reverse("auctions:listings", args=[listing.id]))


def close_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("auctions:index"))


def create_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            comment = Comment(
                auction=listing,
                comment=comment_text,
                author=request.user,
            )
            comment.save()
    return HttpResponseRedirect(reverse("auctions:listings", args=[listing.id]))






