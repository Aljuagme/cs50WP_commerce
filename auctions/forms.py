import datetime
from decimal import Decimal

from django import forms
from .models import Listing


class BidForm(forms.Form):
    place_bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.00'),
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'placeholder': 'Bid higher'
        })
    )

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super().__init__(*args, **kwargs)
        if self.listing:
            # Set min_value to the price of the listing
            if self.listing.current_bid is None:
                min_value = self.listing.price
            else:
                min_value = self.listing.current_bid.bid
            self.fields['place_bid'].min_value = min_value
            self.fields['place_bid'].widget.attrs.update({
                'min': min_value
            })


class ListingForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    price = forms.DecimalField(label='Price', max_digits=5, decimal_places=2)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    category = forms.ChoiceField(
        label='Category',
        choices=Listing.Category.choices,
        initial=Listing.Category.UNCATEGORIZED
    )
    image = forms.URLField(label='Image')



