from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product
from carts.models import Cart


class ProductSlugView(DetailView):
    template_name = 'products/product_details.html'

    # queryset = Product.objects.all()
    def get(self, request, *args, **kwargs):
        context = {}
        try:
            object = self.get_object()
            context['object'] = object
            cart_id, new_cart = Cart.objects.get_cart_id(request)
            cart_obj = Cart.objects.get(id=cart_id)
            context['cart'] = cart_obj
        except:
            return render(request, 'products/product_error.html', {})

        return render(request, self.template_name, context)

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Object not found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404("Unknown error")

        return instance


class ProductIsComingListView(ListView):
    template_name = 'products/products_list_view.html'
    queryset = Product.objects.all().is_coming()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductIsComingListView, self).get_context_data(**kwargs)
        context['is_coming'] = True
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list_view.html'
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        try:
            cart_id, new_cart = Cart.objects.get_cart_id(self.request)
            cart_obj = Cart.objects.get(id=cart_id)
            context['cart'] = cart_obj
        except:
            raise ValueError('No cart')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # print(context)
        return context

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product_obj, is_exists = Product.objects.get_by_id(product_id)
        if is_exists:
            return render(request, self.template_name, {'object': product_obj})
        return render(request, 'products/product_error.html', {})
