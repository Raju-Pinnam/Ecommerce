from django.contrib import admin

from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']


admin.site.register(Cart, CartAdmin)
