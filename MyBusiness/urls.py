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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('Regular/', views.regular_cards, name='Regular'),
    path('Reverse/', views.reverse_cards, name='Reverse'),
    path('Foil/', views.foil_cards, name='Foil'),
    path('Rare/', views.rare_cards, name='Rare'),
    path('Contact/', views.contact, name='contact'),
    path('Cart/', views.cart, name='cart'),
    path('PSA/', views.PSA_Graded, name='PSA'),


]