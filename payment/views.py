from django.shortcuts import render

def payment_success(request):
    return render(request, 'payment/payment_success.html')

def payment_fail(request):
    return render(request, 'payment/payment_fail.html')

def payment_cancel(request):
    return render(request, 'payment/payment_cancel.html')