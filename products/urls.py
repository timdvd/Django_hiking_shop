from django.urls import path, include
from .views import home, product_detail_view, SearchProductView, ProductSlugView

urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>/', ProductSlugView.as_view(), name='product_detail'),
    path('search/', SearchProductView.as_view(), name='search'),
]