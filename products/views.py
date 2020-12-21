from django.shortcuts import render
from .models import Product
from django.http import Http404
from django.views.generic import ListView, DetailView
from carts.models import Cart

# Create your views here.

def home(request):
    context = {
        'title': 'Home',
        'men_products': Product.objects.all().filter(category='men').filter(active=True),
        'women_products': Product.objects.all().filter(category='women').filter(active=True),
        'children_products': Product.objects.all().filter(category='children').filter(active=True),
    }
    return render(request, 'products/home.html', context=context)

def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug, active=True)
    instance = Product.objects.get(slug=slug, active=True)
    image_list = product.images.all()
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    #object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    context = {
        'product': product,
        'images': image_list,
        'cart': cart_obj,
        'title': 'Product',
    }
    return render(request, 'products/detail.html', context)

class ProductSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)

        slug = self.kwargs.get('slug')
        prod_obj = Product.objects.get(slug=slug)
        image_list = prod_obj.images.all()

        context['cart'] = cart_obj
        context['images'] = image_list
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not found')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()

        return instance

class SearchProductView(ListView):
    template_name = 'products/search.html'
    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context