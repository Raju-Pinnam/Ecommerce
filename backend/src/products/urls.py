from django.urls import path

from .views import ProductListView, ProductDetailView, ProductIsComingListView, ProductSlugView

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', ProductSlugView.as_view(), name='product_slug'),
    path('upcoming/', ProductIsComingListView.as_view(), name='product_upcoming'),
]
