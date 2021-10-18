from django.shortcuts import render, redirect
from shopify import Order, PaginatedIterator
from shopify_app.decorators import shop_login_required
from .functions import get_last_order_date, get_orders_dataframe


@shop_login_required
def bengaluru(request):
    if request.method == 'POST':
        last_order_id = str(int(request.POST['last_order_id']) + 1)
        last_order_date = get_last_order_date(last_order_id)

        orders = Order.find( fulfillment_status= "unfulfilled", order="created_at ASC", created_at_min = last_order_date, limit=250)

        df = get_orders_dataframe(orders)
        ord_no = df['Order ID'].tolist()
        return render(request, 'bengaluru.html',{'orders': ord_no})
    else:
        return render(request, 'order_home.html')
