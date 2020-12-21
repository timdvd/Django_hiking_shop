from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
import stripe
from django.http import JsonResponse, HttpResponse
from .models import BillingProfile, Card
from django.conf import settings
import stripe

STRIPE_SECRET_KEY = '' # Your stripe secret key
STRIPE_PUB_KEY = '' # Your stripe publish key
stripe.api_key = STRIPE_SECRET_KEY

def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('cart')
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})

def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({'message', 'Cannot find this user'}, status_code=401)
        token = request.POST.get('token')
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_responce = customer.sources.create(source=token)
            new_card_obj = Card.objects.add_new_card(billing_profile, token) #card_responce
        return JsonResponse({'message': 'Success! Your card was added.'})
    return HttpResponse('error', status_code=401)