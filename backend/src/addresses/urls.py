from django.urls import path

from .views import checkout_address_view, checkout_address_reuse_view

urlpatterns = [
    path('checkout/address/view/', checkout_address_view, name='addresses_ac_view'),
    path('checkout/address/reuse/view/', checkout_address_reuse_view, name='addresses_a_reuse_view'),
]
