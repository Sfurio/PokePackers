# In MyApp/admin.py
from django.contrib import admin
from .models import Card, CardImage, Order, OrderItem

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'series','inventory')

class CardImageAdmin(admin.ModelAdmin):
    list_display = ('card', 'image')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'total_price', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
# Register models
admin.site.register(Card, CardAdmin)
admin.site.register(CardImage, CardImageAdmin)
