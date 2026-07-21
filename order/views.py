# from django.views import generic
# from django.urls import reverse_lazy
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin

# from .forms import CheckoutForm



# class Checkout(LoginRequiredMixin, generic.View):
#     login_url = reverse_lazy('login')

#     def get(self, *args, **kwargs):
#         form = CheckoutForm()

#         return render(
#             self.request,
#             'order/checkout.html',
#             {'form': form}
#         )

#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST)

#         if form.is_valid():
#             return JsonResponse({
#                 'success': True,
#                 'errors': None
#             })

#         return JsonResponse({
#             'success': False,
#             'errors': form.errors
#         })



import uuid

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from cart.carts import Cart

from .forms import CheckoutForm
from .models import Order, OrderItem


class Checkout(LoginRequiredMixin, View):

    login_url = reverse_lazy('login')

    def get(self, request):

        form = CheckoutForm()

        return render(
            request,
            'order/checkout.html',
            {'form': form}
        )

    def post(self, request):

        form = CheckoutForm(request.POST)

        if not form.is_valid():

            return render(
                request,
                'order/checkout.html',
                {'form': form}
            )

        cart = Cart(request)

        transaction_id = str(uuid.uuid4())

        order = Order.objects.create(
            user=request.user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            city=form.cleaned_data['city'],
            zip_code=form.cleaned_data['zip_code'],
            address=form.cleaned_data['address'],
            total=cart.total(),
            paid=False,
            transaction_id=transaction_id,
            status='Pending'
        )

        for item in cart:

            order_item = OrderItem.objects.create(
                product_id=item['product']['id'],
                price=item['product']['price'],
                quantity=item['quantity']
            )

            order.order_items.add(order_item)

        if cart.coupon:
            order.coupon_id = int(cart.coupon)
            order.save()

        request.session['order_id'] = order.id

        return JsonResponse({
            'success': True,
            'redirect_url': '/payment/pay/'
        })