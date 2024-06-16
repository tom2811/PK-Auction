from django.contrib import admin
from .models import User, Element, CardListing, Comment, Bid

# Register your models here.
admin.site.register(User)
admin.site.register(Element)
admin.site.register(CardListing)
admin.site.register(Comment)
admin.site.register(Bid)



