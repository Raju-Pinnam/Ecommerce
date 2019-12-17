from django.db import models


class CartManager(models.Manager):
    def cart_create(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def get_cart_id(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = self.cart_create(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj.id, new_obj


# TODO
    # def get_cart_id(self, request):
    #     del request.session['cart_id']
    #     cart_id = request.session.get('cart_id', None)
    #     print('cart_id', cart_id)
    #     if cart_id is None:
    #         # check user is authenticated or not
    #         if request.user.is_authenticated:
    #             # check user have already a cart_obj
    #             qs = self.model.objects.filter(user=request.user)
    #             if qs.exists():
    #                 # if user have cart id then get that cart id
    #                 cart_obj = qs.first()
    #                 cart_created = False
    #                 # cart_id = cart_obj.id
    #             else:
    #                 # else create cart id for user
    #                 cart_obj = self.model.objects.cart_create(user=request.user)
    #                 cart_created = True
    #                 # assign cart id of user cart id
    #                 # cart_id = cart_obj.
    #         else:
    #             # else user is not authenticated  # TODO check here for guest users
    #             cart_obj = self.model.objects.cart_create(user=None)
    #             cart_created = True
    #             print('cart id as user none')
    #             # create cart id
    #             # cart_id = cart_obj.id
    #             # set cart id to created cart id
    #     else:
    #         # cart id exists
    #         qs = self.model.objects.filter(id=cart_id)
    #         cart_obj = qs.first()
    #         cart_created = False
    #         if request.user.is_authenticated and cart_obj.user is None:
    #             # cart id with user none
    #             # if user authenticated
    #             user_qs = self.model.objects.filter(user=request.user)
    #             # check user has cart or not
    #             if user_qs.exists():
    #                 user_cart_obj = user_qs.first()
    #             else:
    #                 user_cart_obj = self.model.objects.cart_create(user=request.user)
    #                 cart_created = True
    #             selected_products = cart_obj.products.all()
    #
    #             if selected_products is not None:
    #                 for product in selected_products.all():
    #                     if product not in user_cart_obj.products.all():
    #                         user_cart_obj.products.add(product)
    #                         # assign all products to user cart and delete current cart
    #                 user_cart_obj.save()
    #             cart_obj.delete()
    #             cart_obj = user_cart_obj
    #         else:
    #             qs = self.model.objects.filter(id=cart_id)
    #             cart_obj = qs.first()
    #             cart_created = False
    #     # cart id to user cart id
    #     cart_id = cart_obj.id
    #     request.session['cart_id'] = cart_id
    #     return cart_id, cart_created
