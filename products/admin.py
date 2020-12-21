from django.contrib import admin
from .models import Product, ProductImage


class PropertyImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    max_num = 2

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title', 'price']
    list_display = ['title', 'category','price', 'active', 'featured', 'timestamp']
    list_editable = ['price', 'active', 'featured']
    inlines = [ PropertyImageInline, ]
    class Meta:
        model = Product
# Register your models here.
admin.site.register(Product, ProductAdmin)

