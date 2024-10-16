from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Card

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            'home',               # home.html
            'terms',              # terms.html
            'Regular',            # Regular.html
            'Reverse',            # Reverse.html
            'Foil',               # Foil.html
            'Rare',               # Rare.html
            'PSA',                # PSA.html
            'contact',            # Contact.html
            'cart',               # Cart.html
            'checkout',           # checkout.html
            'checkout_success',   # checkout_success.html
        ]

    def location(self, item):
        return reverse(item)


class CardSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Card.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Ensure your `Card` model has an `updated_at` field


# Now include these in your `urls.py` (next step)
