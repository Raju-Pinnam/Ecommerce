from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import ListView

from addresses.models import Address
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm

from .models import Cart


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
    address_form = AddressForm()
    billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id')
    shipping_address_id = request.session.get('shipping_address_id')
    billing_profile, is_billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            # shipping_address = address_qs.filter(address_type='shipping')
            # billing_address = address_qs.filter(address_type='billing')
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id is not None:
            order_obj.shipping_address = Address.objects.filter(id=shipping_address_id).first()
            del request.session['shipping_address_id']
        if billing_address_id is not None:
            order_obj.billing_address = Address.objects.filter(id=billing_address_id).first()
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        "Some check for is order paid or not. These checks are done in payment gateways"
        is_paid = order_obj.mark_paid()
        if is_paid == 'paid':
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect('cart:cart_success')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,
        'address_qs': address_qs,
    }
    return render(request, 'carts/checkout.html', context)


def checkout_done(request):
    return render(request, 'carts/checkout_done.html', {})
