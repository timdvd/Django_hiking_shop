from django.contrib import admin
from .models import Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    search_fields = ['address_type', 'address_line_1', 'address_line_2', 'city', 'postal_code', 'country', 'state']
    list_display = ['billing_profile', 'address_type', 'city','postal_code', 'country', 'state']
    class Meta:
        model = Address


admin.site.register(Address, AddressAdmin)
