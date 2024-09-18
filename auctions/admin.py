from django.contrib import admin

from auctions.models import Listing, Comment, Bid, User


# Register your models here.
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "author", "created_at")


admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)