from django.urls import path

from .views import CartHome, CartUpdate, checkout_home, checkout_done, cart_detail_api_view

urlpatterns = [
    path('', CartHome.as_view(), name='cart_home'),
    path('checkout/', checkout_home, name='cart_checkout'),
    path('cart_update/', CartUpdate.as_view(), name='cart_update'),
    path('cart_success/', checkout_done, name='cart_success'),
    path('api/', cart_detail_api_view, name='cart_api'),
]
