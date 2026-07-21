from django.http import HttpResponse
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from order.models import Order
from cart.carts import Cart

@csrf_exempt
def payment_success(request):

    tran_id = request.POST.get('tran_id')

    order = Order.objects.filter(
        transaction_id=tran_id
    ).first()

    if order:
        order.paid = True
        order.status = 'Received'
        order.save()

        cart = Cart(request)
        cart.clear()

    return render(
        request,
        'payment/payment_success.html',
        {
            'order': order,
            'transaction_id': tran_id
        }
    )


@csrf_exempt
def payment_fail(request):

    tran_id = request.POST.get('tran_id')

    order = Order.objects.filter(
        transaction_id=tran_id
    ).first()

    if order:
        order.status = 'Cancelled'
        order.save()

    return render(
        request,
        'payment/payment_fail.html'
    )

@csrf_exempt
def payment_cancel(request):

    tran_id = request.POST.get('tran_id')

    order = Order.objects.filter(
        transaction_id=tran_id
    ).first()

    if order:
        order.status = 'Cancelled'
        order.save()

    return render(
        request,
        'payment/payment_cancel.html'
    )

def sslcommerz_payment(request):

    order_id = request.session.get('order_id')

    if not order_id:
        return redirect('cart')

    order = Order.objects.get(id=order_id)

    settings_data = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_pass': settings.SSLCOMMERZ_STORE_PASSWORD,
        'issandbox': settings.SSLCOMMERZ_SANDBOX
    }

    sslcz = SSLCOMMERZ(settings_data)

    post_body = {}

    post_body['total_amount'] = float(order.total)
    post_body['currency'] = "BDT"
    post_body['tran_id'] = str(order.transaction_id)

    post_body['success_url'] = request.build_absolute_uri('/payment/success/')
    post_body['fail_url'] = request.build_absolute_uri('/payment/fail/')
    post_body['cancel_url'] = request.build_absolute_uri('/payment/cancel/')
    post_body['ipn_url'] = request.build_absolute_uri('/payment/success/')

    post_body['cus_name'] = f"{order.first_name} {order.last_name}"
    post_body['cus_email'] = order.email
    post_body['cus_add1'] = order.address
    post_body['cus_city'] = order.city
    post_body['cus_postcode'] = order.zip_code
    post_body['cus_country'] = "Bangladesh"
    post_body['cus_phone'] = "01700000000"

    post_body['shipping_method'] = "Courier"
    post_body['product_name'] = "Ecommerce Order"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    post_body['ship_name'] = f"{order.first_name} {order.last_name}"
    post_body['ship_add1'] = order.address
    post_body['ship_city'] = order.city
    post_body['ship_postcode'] = order.zip_code
    post_body['ship_country'] = "Bangladesh"

    response = sslcz.createSession(post_body)

    print(response)

    if response.get('status') == 'SUCCESS':
        return redirect(response['GatewayPageURL'])

    return HttpResponse(
        f"SSLCommerz Error: {response.get('failedreason')}"
    )