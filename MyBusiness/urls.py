from django.contrib import admin
from django.urls import path
from MyApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView  # For serving robots.txt
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
    path('Cart/', views.cart, name='cart'),  # You can keep this or 'cart/' (case matters)
    path('PSA/', views.PSA_Graded, name='PSA'),
    path('add_to_cart/<int:card_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('card/<int:card_id>/', views.card_detail, name='card_detail'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/success/', views.checkout_success_view, name='checkout_success'),

    # Robots.txt using TemplateView
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)