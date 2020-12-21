from django.contrib import admin
from .models import BillingProfile, Card, Charge

class BillingProfileAdmin(admin.ModelAdmin):
    search_fields = ['email', 'customer_id']
    list_display = ['email','customer_id', 'active', 'timestamp']
    list_editable = ['active']
    class Meta:
        model = BillingProfile

class ChargeAdmin(admin.ModelAdmin):
    search_fields = ['stripe_id']
    list_display = ['stripe_id' ,'paid', 'refunded', 'risk_level']
    list_editable = ['paid','refunded',]
    class Meta:
        model = Charge

admin.site.register(BillingProfile, BillingProfileAdmin)
admin.site.register(Card)
admin.site.register(Charge, ChargeAdmin)