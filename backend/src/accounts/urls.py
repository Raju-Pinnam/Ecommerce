from django.urls import path
from .views import LoginUser, Logout, RegisterUser, guest_register

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/guest/', guest_register, name='guest_view'),
    path('register/', RegisterUser.as_view(), name='register')
]
