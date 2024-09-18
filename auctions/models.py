from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import HiddenInput


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")

class Listing(models.Model):
    class Category(models.TextChoices):
        FASHION = 'FA', 'Fashion'
        TOYS = 'TO', 'Toys'
        ELECTRONICS = 'EL', 'Electronics'
        HOME = 'HO', 'Home'
        UNCATEGORIZED = 'UC', 'Uncategorized'

    class Meta:
        ordering = ['-created_at']


    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey('Bid', on_delete=models.SET_NULL, related_name="highest_bid", null=True)
    n_bids = models.IntegerField(default=0)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.UNCATEGORIZED)
    image = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_category_display(self):
        return self.Category(self.category).label # To pass it to django

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.bid}"


class Comment(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.auction} commented: {self.comment}"
