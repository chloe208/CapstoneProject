import time
from django.shortcuts import render, redirect
from carts.models import Cart
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from decimal import Decimal

from .models import Order

from .utils import id_generator

def orders(request): 
    context ={}
    template = 'orders/user.html'
    return render(request, template, context)


