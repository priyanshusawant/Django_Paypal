import uuid

from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm 
from django.conf import settings

# Create your views here.

def home(request):
    host = request.get_host()
    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '20.00',
        'item_name':'Product 1',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial= paypal_dict)
    context = {
        'form':form
    }
    return render(request, 'home.html', context)

def paypal_return(request):
    messages.success(request, 'You\'ve successfully made a payment!')
    return redirect('home')

def paypal_cancel(request):
    messages.error(request, 'Your order has been cancelled.')
    return redirect('home')
