"""
URL configuration for MyBusiness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MyApp import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from MyApp.sitemaps import StaticViewSitemap, CardSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'cards': CardSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('terms/', views.terms, name='terms'),
    path('home/', views.home, name='home'),
    path('Regular/', views.regular_cards, name='Regular'),
    path('Reverse/', views.reverse_cards, name='Reverse'),
    path('Foil/', views.foil_cards, name='Foil'),
    path('Rare/', views.rare_cards, name='Rare'),
    path('Contact/', views.contact, name='contact'),
    path('Cart/', views.cart, name='cart'),
    path('PSA/', views.PSA_Graded, name='PSA'),
    path('add_to_cart/<int:card_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('check-stripe-keys/', views.check_stripe_keys_view, name='check_stripe_keys'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)