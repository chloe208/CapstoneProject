"""colormethis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
admin.autodiscover()
from django.urls import path, include, re_path

# to connect the link from products app
from products import views as cmt # products
from carts import views as cart
from orders import views as order
from favorites import views as fav
# for login
from django.contrib.auth import views as auth_views
from django.urls import path
#for register
from users import views as user_views
# from carts.views import view, add_to_cart

# for static files
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),
    # HOME
    path('', cmt.home),
    path('home/', cmt.home),
    # SEARCH URL
    path('s/', cmt.search, name='search'),
    # PRODUCTS
    path('products/', cmt.showall, name='products'),
    path('products/<slug:slug>/', cmt.single, name='single_product'),
    # REGISTER
    path('register/', user_views.register, name='register'),
    # LOGIN/LOGOUT
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    # PROFILE
    path('profile/', user_views.profile, name='profile'),
    # CRS 
    path('upload/',cmt.upload, name='find_my_shade'),
    path('colorMatch/', cmt.color_match, name='color_match'),
    # ABOUT US
    path('aboutus/', cmt.aboutus, name='about_us'),
    # CARTS
    path('cart/', cart.view, name='cart'),
    path('checkout/', cart.checkout, name='checkout'),
    path('orders/', order.orders, name='user_orders'),
    path('cart/<int:id>/', cart.remove_from_cart, name='remove_from_cart'),
    path('cart/<slug:slug>/', cart.add_to_cart, name='add_to_cart'),
    # FAVORITES
    path('favorite/', fav.view, name='favorite'),
    # path('cart/<int:id>/', cart.remove_from_cart, name='remove_from_cart'),
    path('favorite/<slug:slug>/', fav.update_favorite, name='update_favorite'),
    path('products/<slug:slug>/comment/', cmt.add_comment, name='comment'),
    # CHECKOUT TRIAL
    path('checkitout/', cart.checkout_home, name='checkitout'), 
    # Sort by brand
    path('mac/', cmt.mac, name='mac' ),
    path('maybelline/', cmt.maybelline, name='maybelline' ),
    path('bobbibrown/', cmt.bobbibrown, name='bobbibrown' ),

    # Sort by makeup_type
    path('lipstick/', cmt.lipstick, name='lipstick' ),
    path('foundation/', cmt.foundation, name='foundation' ),

    # PAYPAL
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/', cart.process_payment, name='process_payment'),
    path('thank-you/', cart.payment_done, name='payment_done'),
    path('payment-canceled/', cart.payment_canceled, name='payment_canceled'),

]

# +static is to load static files

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
