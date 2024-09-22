# In MyApp/admin.py
from django.contrib import admin
from .models import Card, CardImage

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'series','inventory')

class CardImageAdmin(admin.ModelAdmin):
    list_display = ('card', 'image')

# Register models
admin.site.register(Card, CardAdmin)
admin.site.register(CardImage, CardImageAdmin)
