from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from .models import Favorite


# import from other apps
from products.models import Product

# VIEWS IS FOR URL VIEW

def view(request):
    # return render(request, 'favorite/view.html', {})
    favorite = Favorite.objects.all()[0]
    context= {"favorite": favorite}
    template = "favorite/view.html"
    return render(request, template, context) 

def update_favorite(request, slug):
    favorite = Favorite.objects.all()[0]
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not product in favorite.products.all():
        favorite.products.add(product)
    else:
        favorite.products.remove(product)
    return HttpResponseRedirect(reverse("favorite"))
    # return render(request, template, context)

def fav_to_cart(request, slug):
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
