from django.contrib import admin
from .models import GuestEmail, Profile
from django.contrib.auth.models import User

class UserAdmin():
    pass

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail

admin.site.register(Profile)
admin.site.register(GuestEmail, GuestEmailAdmin)