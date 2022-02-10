from django.shortcuts import render, redirect
from shopify import Order, PaginatedIterator
from shopify_app.decorators import shop_login_required
from django.contrib.auth.decorators import login_required
from .functions import get_last_order_date, get_orders_dataframe
import pandas as pd
from .models import Amzonproducts
from .utils import data_transform, iter_pd, pandas_to_sheets, get_credentials
from django.conf import settings

import string


@shop_login_required
@login_required(login_url="/accounts/login")
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

@login_required(login_url="/accounts/login")
def amazon(request):
    if request.method == 'POST':

        txt_file = request.FILES['file']

        if not txt_file.name.endswith('.txt'):
            messages.error(request, 'THIS IS NOT A TXT FILE')

        df = pd.read_csv(txt_file, sep="\t", header=0)
        df, msg = data_transform(df)
        msg1 = {}
        if len(msg) == 0:
            msg1['message'] = "Order processed"

        gc = get_credentials()
        workbook = gc.open_by_key(settings.SPREADSHEET_KEY)
        df1 = df[['Order ID','Date & Time of Order creation','title','packs','Courier']]
        df.drop('packs', axis=1, inplace=True)
        worksheet = workbook.worksheet("Master Sheet")
        l = list(string.ascii_uppercase)
        (row, col) = df.shape
        val = worksheet.get_all_values()
        cells = worksheet.range("A{}:M{}".format(len(val)+1, len(val)+len(df)+1))
        for cell, val in zip(cells, iter_pd(df)):
            cell.value = val
        worksheet.update_cells(cells)

        couriers = ["BNG","MUM","DL"]
        for c in couriers:
            if (df1['Courier'] == c).sum() > 0:
                df2 = df1[df1['Courier'] == c]
                worksheet = workbook.worksheet(c)
                val = worksheet.get_all_values()
                df2['Sl No.'] = [i for i in range(len(val), len(val)+len(df2))]
                cells = worksheet.range("A{}:E{}".format(len(val)+1, len(val)+len(df2)+1))
                for cell, val in zip(cells, iter_pd(df2[['Sl No.','Date & Time of Order creation','Order ID','title','packs']])):
                    cell.value = val
                worksheet.update_cells(cells)

        return render(request, 'amazon.html', {'msg':msg,'msg1':msg1})

    else:
        return render(request, 'amazon.html')
