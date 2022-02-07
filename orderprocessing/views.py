from django.shortcuts import render, redirect
from shopify import Order, PaginatedIterator
from shopify_app.decorators import shop_login_required
from django.contrib.auth.decorators import login_required
from .functions import get_last_order_date, get_orders_dataframe
import pandas as pd
from .models import Amzonproducts
from .utils import data_transform, iter_pd, pandas_to_sheets
from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
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

        cred = {
                "type": settings.TYPE,
                "project_id" : settings.PROJECT_ID,
                "private_key_id" : settings.PRIVATE_KEY_ID,
                "client_id" : settings.CLIENT_ID,
                "auth_uri" : settings.AUTH_URI,
                "token_uri" : settings.TOKEN_URI,
                "auth_provider_x509_cert_url" : settings.AUTH_PROVIDER_X509_CERT_URL,
                "client_x509_cert_url" : settings.CLIENT_X509_CERT_URL,
                "private_key" : settings.PRIVATE_KEY,
                "client_email": settings.CLIENT_EMAIL
                }

        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred, scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(settings.SPREADSHEET_KEY)
        worksheet = workbook.worksheet("Master Sheet")
        pandas_to_sheets(dd, worksheet)

        return render(request, 'amazon.html', {'msg':msg,'msg1':msg1})

    else:
        return render(request, 'amazon.html')
