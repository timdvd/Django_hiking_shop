from django.db import models
from django.urls import reverse
from django.db.models import Q
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
# Create your models here.

CATEGORY_CHOICES = (
    ('men', 'Men'),
    ('women', 'Women'),
    ('children', 'Children'),
)
class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    def all(self):
        return self.get_queryset().active()
    def search(self, query):
        lookups = Q(title__icontains=query) | Q(price__icontains=query) | Q(category__icontains=query)
        return self.get_queryset().active().filter(lookups).distinct()

class Product(models.Model):
    title       = models.CharField(max_length=50)
    category    = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image       = models.ImageField(upload_to='prod_pics', default='')
    price       = models.DecimalField(max_digits=100, decimal_places=2)
    active      = models.BooleanField(default=True)
    featured    = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    slug        = models.SlugField(unique=True, null=True, blank=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prod_pics')


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)