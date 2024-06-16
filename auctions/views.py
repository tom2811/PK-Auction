from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Element, CardListing, Comment, Bid


def index(request):
    activeListings = CardListing.objects.filter(isActive=True)
    allElements = Element.objects.all()
    watchlist_count = request.user.listingWatchlist.count() if request.user.is_authenticated else 0
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "elements": allElements,
        "watchlist_count": watchlist_count,
    })

def listing(request, id):
    listingData = CardListing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    elementType = listingData.listingType.elementType if listingData.listingType else "---"
    watchlist_count = request.user.listingWatchlist.count() if request.user.is_authenticated else 0
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "elementType": elementType,
        "watchlist_count": watchlist_count,
    })

def addComment(request, id):
    currentUser = request.user
    listingData = CardListing.objects.get(pk=id)
    message = request.POST['comment']

    newComment = Comment(
        author = currentUser,
        listing = listingData,
        message = message
    )
    
    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def displayWatchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    watchlist_count = currentUser.listingWatchlist.count()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist_count": watchlist_count,
    })

def removeWatchlist(request, id):
    listingData = CardListing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchlist(request,id ):
    listingData = CardListing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))
    
def categories(request):
    allElements = Element.objects.all()

    watchlist_count = 0
    if request.user.is_authenticated:
        watchlist_count = request.user.listingWatchlist.count()

    if request.method == "POST":
        formType = request.POST.get("type")
        
        if not formType or formType == "---":
            activeListings = [] 
            selected_type = None
        else:
            try:
                type = Element.objects.get(elementType=formType)
                activeListings = CardListing.objects.filter(isActive=True, listingType=type)
                selected_type = type
            except Element.DoesNotExist:
                activeListings = []
                selected_type = None
        
        return render(request, "auctions/categories.html", {
            "listings": activeListings,
            "elements": allElements,
            "selected_type": selected_type,
            "watchlist_count": watchlist_count,
        })
    
    activeListings = []
    return render(request, "auctions/categories.html", {
        "listings": activeListings,
        "elements": allElements,
        "selected_type": None,
        "watchlist_count": watchlist_count,
    })

def addListing(request):
    if request.method == "GET":
        allElements = Element.objects.all()
        watchlist_count = 0
        if request.user.is_authenticated:
            watchlist_count = request.user.listingWatchlist.count()

        return render(request, "auctions/add.html", {
            "elements": allElements,
            "watchlist_count": watchlist_count,
        })
    else:
        name = request.POST['name']
        price = request.POST["price"]
        imageUrl = request.POST["imageUrl"]
        type = request.POST["type"]
        currentUser = request.user

        errors = {}
        if not name:
            errors["name"] = "Name is required."
        if not price:
            errors["price"] = "Price is required."
        if not imageUrl:
            errors["imageUrl"] = "Image URL is required."
        if not type:
            errors["type"] = "Type is required."

        if errors:
            allElements = Element.objects.all()
            watchlist_count = request.user.listingWatchlist.count()
            return render(request, "auctions/add.html", {
                "elements": allElements,
                "errors": errors,
                "watchlist_count": watchlist_count,
            })

        try:
            elementData = Element.objects.get(elementType=type)
        except Element.DoesNotExist:
            messages.error(request, f"Element type '{type}' does not exist.")
            return redirect(reverse("add_listing"))

        bid = Bid(bid=float(price), user=currentUser)
        bid.save()

        newListing = CardListing(
            name=name,
            price=bid,
            imageUrl=imageUrl,
            listingType=elementData,
            owner=currentUser
        )

        newListing.save()
        return HttpResponseRedirect(reverse("index"))
    
def addBid(request, id):
    newBid = request.POST["bid"]
    listingData = CardListing.objects.get(pk=id)
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    if int(newBid) > listingData.price.bid:
        updatedBid = Bid(user=request.user, bid=int(newBid))
        updatedBid.save()
        listingData.price = updatedBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid Updated Successfully!",
            "updated": True,
            "isOwner": isOwner,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Bid Failed to Update",
            "updated": False,
            "isListingInWatchlist": isListingInWatchlist,
            "allComments": allComments,
            "isOwner": isOwner,
        })
        
def closeAuction(request, id):
    listingData = CardListing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isOwner = request.user.username == listingData.owner.username
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allComments": allComments,
        "isOwner": isOwner,
        "updated": True,
        "message": "Auction Closed!"
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
