from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Element(models.Model):
    elementType = models.CharField(max_length=64)
    
    def __str__(self):
        return self.elementType
    
class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

class CardListing(models.Model):
    name = models.CharField(max_length=64)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    imageUrl = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    listingType = models.ForeignKey(Element, on_delete=models.CASCADE, blank=True, null=True, related_name="element")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(CardListing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    message = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"

