from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


class ProductSearchView(ListView):
    template_name = 'search/search_view.html'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()

    def get(self, request, *args, **kwargs):
        context = {}
        object_list = self.get_queryset()
        context['query'] = request.GET.get('q')
        if object_list.exists():
            context['object_list'] = object_list
            return render(request, self.template_name, context)
        return render(request, 'products/product_error.html', context)
