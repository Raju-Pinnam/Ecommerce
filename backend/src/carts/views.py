from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView

from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile

from .models import Cart
from accounts.models import GuestUser


class CartHome(ListView):
    template_name = 'carts/cart_home.html'

    def get(self, request, *args, **kwargs):
        cart_id, new_cart = Cart.objects.get_cart_id(request)
        cart_obj = Cart.objects.get(id=cart_id)
        context = {
            'cart': cart_obj
        }
        request.session['cart_items'] = cart_obj.products.count()
        return render(request, self.template_name, context)


class CartUpdate(View):

    def post(self, request, *args, **kwargs):
        cart_obj = None
        product_id = request.POST.get('product_id', '')
        print(product_id)
        if product_id is not None:
            product_obj = Product.objects.get(id=product_id)
            cart_id, new_cart = Cart.objects.get_cart_id(request)
            cart_obj = Cart.objects.get(id=cart_id)
            if product_obj in cart_obj.products.all():
                cart_obj.products.remove(product_obj)
            else:
                cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        return redirect('cart:cart_home')


def checkout_home(request):
    cart_id, new_cart = Cart.objects.get_cart_id(request)
    cart_obj = Cart.objects.get(id=cart_id)
    order_obj = None
    if new_cart or cart_obj.products.count() == 0:
        return redirect('cart:cart_home')

    login_form = LoginForm()
    guest_form = GuestForm()
    billing_profile, is_billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    return render(request, 'carts/checkout.html', context)
