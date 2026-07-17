from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutForm



class Checkout(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('login')

    def get(self, *args, **kwargs):
        form = CheckoutForm()

        return render(
            self.request,
            'order/checkout.html',
            {'form': form}
        )

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)

        if form.is_valid():
            return JsonResponse({
                'success': True,
                'errors': None
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        })