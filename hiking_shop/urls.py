"""hiking_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import user_register
from addresses.views import checkout_address_create, checkout_address_reuse_view
from billing.views import payment_method_create_view, payment_method_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('cart/', include('carts.urls')),
    path('user/', include('users.urls')),
    path('billing/payment-method/', payment_method_view, name='payment-method'),
    path('billing/payment-method/create/', payment_method_create_view, name='payment-method-create'),
    path('checkout/address/create/', checkout_address_create, name='checkout_address'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)