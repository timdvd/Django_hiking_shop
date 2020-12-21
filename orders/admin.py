from django.contrib import admin
from .models import Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id', 'shipping_address', 'billing_address']
    list_display = ['order_id', 'status','order_total', 'active', 'timestamp']
    list_editable = ['status', 'active']
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
