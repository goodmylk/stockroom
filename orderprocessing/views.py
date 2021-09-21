from django.shortcuts import render, redirect
import shopify
from shopify_app.decorators import shop_login_required

@shop_login_required
def bengaluru(request):
    products = shopify.Product.find(limit=3)
    orders = shopify.Order.find(limit=3, order="created_at DESC")
    return render(request, 'bengaluru.html',{'products': products, 'orders': orders})
