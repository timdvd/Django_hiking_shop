from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)

# Create your models here.
class Address(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type        = models.CharField(max_length=100, choices=ADDRESS_TYPES)
    address_line_1      = models.CharField(max_length=100)
    address_line_2      = models.CharField(max_length=100, null=True, blank=True)
    city                = models.CharField(max_length=60)
    postal_code         = models.CharField(max_length=60)
    country             = models.CharField(max_length=60, default='United States of America')
    state               = models.CharField(max_length=120)

    def __str__(self):
        return f"{str(self.billing_profile)} --> {self.address_type}"  

    def get_address(self):
        return '{}\n{}\n{}\n{}\n{}\n'.format(self.address_line_1, self.address_line_2, self.city, self.postal_code, self.country)
