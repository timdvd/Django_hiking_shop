from django.contrib import admin
from .models import Cart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'updated','timestamp']
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)