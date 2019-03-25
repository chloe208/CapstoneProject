# Create your views here.
# This is connected to URLs
from django.shortcuts import render,redirect
from django.urls import reverse
from orders.utils import id_generator
from orders.models import Order
from carts.models import Cart
from billing.models import BillingProfile
# to grab things from Product, Cart
from products.models import Product, Variation
from .models import Cart, CartItem
# for login
from django.contrib.auth.decorators import login_required
# paypal
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


# PAYPAL
def process_payment(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
 
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.update_total().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'CAD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process_payment.html', {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/payment_done.html')
 
 
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment_cancelled.html')


#require user login
@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return redirect(reverse("cart"))
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        request.session['order_id'] = str(new_order.order_id)
        new_order.save()
    except:
        #work on some error message
        return redirect("process_payment")
 
    #run credit card
    if new_order.status == "Finished":
        #cart.delete()
        del request.session['cart_id']
        del request.session['items_total']
        return redirect(reverse("cart"))
    context = {}
    template="cart/checkout.html"
    return render(request, template, context)

@login_required
def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:view")
    else:    
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user=request.user
    if user.is_authenticated():
        billing_profile=None
    return render(request, "cart/checkitout.html", {"object": order_obj})

def view(request):
    # if no user it appears like this.
    try:
        the_id = request.session['cart_id']
        cart=Cart.objects.get(id=the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        request.session['total'] = new_total
        request.session['shipping_fee'] = 6.99
        request.session['tax_total'] = new_total*0.13
        request.session['final_total'] = new_total *1.13 + 6.99
        cart.total = new_total
        cart.save()
  
        context={"cart":cart}
    else:
        empty_message="Your cart is empty, please keep shopping."
        context ={"empty":True, "empty_message":empty_message}

    template = 'cart/view.html'
    return render(request, template, context)

def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart=Cart.objects.get(id=the_id)
    except:
        return redirect(reverse("cart"))

    cartitem = CartItem.objects.get(id=id)
    cartitem.cart = None
    cartitem.save()
    return redirect(reverse("cart"))



def add_to_cart(request, slug):
    #Session is set to expire in 5 mins = 3000
    request.session.set_expiry(3000)
    # PRODUCT QUANTITY
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart() 
        new_cart.save()
        request.session['cart_id']=new_cart.id
        the_id=new_cart.id

    cart = Cart.objects.get(id=the_id)
    #ITEMS IN CART
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass
    product_var = [] #product_var

    if request.method == "POST":
        qty = request.POST['qty']
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                product_var.append(v)
            except:
                pass
        cart_item = CartItem.objects.create(cart=cart, product=product)
        print(cart_item)
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
    # saving notes in a dictionary
        cart_item.save()
        # success message
        return redirect(reverse("cart"))
    #error message
    return redirect(reverse("cart"))

