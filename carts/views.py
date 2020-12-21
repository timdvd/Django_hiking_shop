from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from orders.models import Order
from django.db.models.signals import pre_save, post_save
from users.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from users.models import GuestEmail
from django.http import JsonResponse
from addresses.forms import AddressForm
from addresses.models import Address
from django.conf import settings
from django.urls import reverse
import stripe
# Create your views here.

STRIPE_SECRET_KEY = '' # Your stripe secret key
STRIPE_PUB_KEY = '' # Your stripe public key
stripe.api_key = STRIPE_SECRET_KEY

def cart(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/cart.html", {"cart": cart_obj})

def cart_update(request, slug):
    if slug is not None:
        product_obj = Product.objects.get(slug=slug)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if not product_obj in cart_obj.products.all():
            cart_obj.products.add(product_obj)
            added = True
    return redirect('cart')

def cart_delete(request, slug):
    if slug is not None:
        product_obj = Product.objects.get(slug=slug)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
    return redirect('cart')

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart")  
    
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id) 
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_done()
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                return redirect("done/")
            else:
                return redirect("done/")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, "carts/checkout.html", context)


def checkout_done(request):
    return render(request, 'carts/checkout-done.html', {})
