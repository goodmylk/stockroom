import pandas as pd
from .models import Box, Amzonproducts
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings

def filter_orders(orders):
    if orders['title'].isnull().sum() > 0:
        to_drop = orders[orders['title'].isnull()]['Order ID'].tolist()
        return to_drop
    else:
        return []


def get_credentials():
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
    return gspread.authorize(credentials)


def get_volumetric_weight(product):
    pr2 = pd.pivot(product.groupby(['Order ID','contents'], as_index=False).agg({'pack':'sum'}), columns='contents', index='Order ID')
    pr2.columns = [x[-1] for x in pr2.columns]
    pr2  = pr2.fillna(0)

    if 'Mayo, Butter' not in pr2.columns:
        pr2['Mayo, Butter'] = 0

    if 'Mayo' not in pr2.columns:
        pr2['Mayo'] = 0

    if 'No sugar mylk' not in pr2.columns:
        pr2['No sugar mylk'] = 0

    if 'Butter' not in pr2.columns:
        pr2['Butter'] = 0

    if 'Choc mylk' not in pr2.columns:
        pr2['Choc mylk'] = 0

    if 'Mylk' not in pr2.columns:
        pr2['Mylk'] = 0

    if 'Mylk 1L' not in pr2.columns:
        pr2['Mylk 1L'] = 0

    if 'No sugar mylk 1L' not in pr2.columns:
        pr2['No sugar mylk 1L'] = 0

    if 'Parmesan' not in pr2.columns:
        pr2['Parmesan'] = 0

    pr2['Mayo'] = pr2['Mayo, Butter']//2 + pr2['Mayo']
    pr2['Butter'] = pr2['Mayo, Butter']//2 + pr2['Butter']
    pr2['Mylk'] = pr2['Mylk'] + pr2['Choc mylk'] + pr2['No sugar mylk']
    pr2 = pr2.drop(['Choc mylk','No sugar mylk'], axis=1)
    pr2 = pr2.reset_index()

    l = []
    for order_id in pr2['Order ID']:

        tt = pd.DataFrame(list(Box.objects.all().values()))
        mk = pr2[pr2['Order ID'] == order_id]['Mylk'].tolist()[0]

        tt = tt[tt['mylk'] > mk]
        tt['butter'] = round(tt['butter'] - mk*(tt['butter'] / tt['mylk']),0)
        tt['mayo'] = round(tt['mayo'] - mk*(tt['mayo'] / tt['mylk']),0)

        mk = pr2[pr2['Order ID'] == order_id]['Butter'].tolist()[0]

        tt = tt[tt['butter'] > mk]
        tt['mayo'] = round(tt['mayo'] - mk*(tt['mayo'] / tt['butter']),0)

        mk = pr2[pr2['Order ID'] == order_id]['Mayo'].tolist()[0]
        tt = tt[tt['mayo'] > mk]

        if len(tt) == 0:
            l.append('G')
        else:
            l.append(tt['Box'].min())

    bx = pd.DataFrame(list(Box.objects.all().values()))
    pr2['Box'] = l
    pr2 = pd.merge(pr2[['Order ID','Box']], bx[['Box','Height','Length','Width']], on='Box', how='left')
    pr2['volumetric weight'] = pr2['Height']*pr2['Length']*pr2['Width'] / 4000
    return pr2[['Order ID','volumetric weight']]

def data_transform(df):
    df.columns = df.columns.str.replace('order-id','Order ID')

    amz = pd.DataFrame(list(Amzonproducts.objects.all().values()))
    df1 = pd.merge(df, amz, on='sku', how='left')

    to_drop = filter_orders(df1)
    msg = {}
    if len(to_drop) > 0:
        df = df[~df['Order ID'].isin(to_drop)]
        if len(to_drop) == 1:
            msg['message'] = f'{to_drop[0]} order not processed.'
        else:
            s = ','.join(to_drop)
            msg['message'] = f'{s} orders not processed.'

    df['Parcel'] = 'goodmylk'
    df['cod_amount'] = 0
    df['Customer Name'] = df['recipient-name'].str.title()
    df.columns = df.columns.str.replace('buyer-phone-number','Mobile')
    df['ship-address-3'] = df['ship-address-3'].fillna('')
    df['ship-address-2'] = df['ship-address-2'].fillna('')
    df['ship-address-1'] = df['ship-address-1'].fillna('')
    df['Address'] = df['ship-address-1'] + ', ' + df['ship-address-2'] + ', '+ df['ship-address-3'] + ', '+ df['ship-city']
    df.columns = df.columns.str.replace('ship-postal-code','Pincode')
    df.columns = df.columns.str.replace('purchase-date','Date & Time of Order creation')
    df['Date & Time of Order creation'] = df['Date & Time of Order creation'].str.replace('T',' ')

    pr = pd.merge(amz, df[['Order ID','sku','quantity-to-ship']], on='sku', how='right')
    pr['pack'] = pr['quantity-to-ship'] * pr['pack']
    pr['pack1'] = pr['pack'].apply(lambda x: str(x))
    pr1 = pr.groupby('Order ID', as_index=False).agg({'title': ','.join,'contents': ','.join, 'pack':'sum', 'weight':'sum','price':'sum','pack1':','.join})
    pr1.columns = ['Order ID', 'title', 'contents', 'no of packs', 'weight','total_price','packs']

    df = pd.merge(df, pr1, on='Order ID', how='left')

    pr2 = get_volumetric_weight(pr)
    df = pd.merge(df, pr2, on='Order ID' , how='left')
    df['weight'] = df['weight'] + 300
    df['weight']  = df['weight']/1000

    l= []
    for x, y in zip(df['weight'], df['volumetric weight']):
        if x >= y:
            l.append(x)
        else:
            l.append(y)

    df['final weight'] = l

    st = ['Karnataka','Goa','Telangana', 'Andhra Pradesh','Kerala','Tamil Nadu']
    st_nd = ['Delhi','Ladakh', 'Jammu and Kashmir', 'Punjab', 'Himachal Pradesh', 'Uttarakhand', 'Haryana', 'Uttar Pradesh', 'Rajasthan', 'Bihar',
             'Jharkhand', 'West Bengal', 'Sikkim', "Manipur", 'Assam', 'Arunachal Pradesh', 'Mizoram', 'Nagaland', 'Tripura', 'Meghalaya']

    df['Courier'] =  df['ship-state'].str.title().apply(lambda x: 'BNG' if x in st
                                                  else 'DL' if x in st_nd
                                                  else 'MUM')

    df = df.drop_duplicates()
    df = df[['Parcel','cod_amount','Customer Name','Mobile','Address','Pincode','Order ID','total_price','no of packs','final weight','title','Courier','Date & Time of Order creation','packs']]

    return df, msg

def iter_pd(df):
    for row in df.to_numpy():
        for val in row:
            if pd.isna(val):
                yield ""
            else:
                yield val


def pandas_to_sheets(pandas_df, sheet, clear = False):
    # Updates all values in a workbook to match a pandas dataframe
    if clear:
        sheet.clear()
    (row, col) = pandas_df.shape
    cells = sheet.range("A1:{}".format(gspread.utils.rowcol_to_a1(row + 1, col)))
    for cell, val in zip(cells, iter_pd(pandas_df)):
        cell.value = val
    sheet.update_cells(cells)
