from django.urls import path

from .views import HomePage, ContactPage

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contact/', ContactPage.as_view(), name='contact'),
]
