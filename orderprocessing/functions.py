from shopify import Order, PaginatedIterator
import pandas as pd

def get_last_order_date(last_order_id):
    last_order = Order.find(name=last_order_id)
    for page in PaginatedIterator(last_order):
        for item in page:
            last_order_date = item.created_at
    return last_order_date

def get_orders_dataframe(order_object, panindia=True):
    orders = []
    if panindia:
        for page in PaginatedIterator(order_object):
            for item in page:
                    if 'panindia' in item.tags.lower():
                        order = []
                        order.append(item.name)
                        order.append(item.shipping_address)
                        order.append(item.line_items)
                        order.append(item.shipping_lines)
                        order.append(item.tags)
                        orders.append(order)

        df = pd.DataFrame(orders, columns=['Order ID','shipping_address','line_items','shipping_lines','tags'])

        #Customer Details
        name = []
        for x  in df['shipping_address']:
            if type(x) == float:
                name.append('NA')
            else:
                if ((x.last_name == '') | (x.last_name == None)):
                    name.append(x.first_name)
                else:
                    name.append(x.first_name + ' '+ x.last_name)

        df['Name'] = name
        df['Name'] = df['Name'].apply(lambda x: x.title())

        df['Phone'] = df['shipping_address'].apply(lambda x: x.phone if type(x) != float else 'NA')
        df['Phone'] = df['Phone'].apply(lambda x: x.strip().replace(' ',''))
        df['Phone'] = df['Phone'].apply(lambda x: 'Not available' if len(x) == 0 else x)
        df['Phone'] = df['Phone'].apply(lambda x: x[1:] if x[0] == '0'
                           else x[3:] if x[0:3] == '+91'
                           else x[2:] if ((len(x) == 12) & (x[0:2] == '91'))
                           else x)

       #Shipping address
        address = []
        for x  in df['shipping_address']:
            if type(x) == float:
                address.append('NA')
            else:
                if ((x.address2 == '') | (x.address2 == None)):
                    address.append(x.address1)
                else:
                    address.append(x.address1 + ' '+ x.address2)

        df['Address'] = address
        df['Pincode'] = df['shipping_address'].apply(lambda x: x.zip if type(x) != float else 'NA')
        df['Address']  = df['Address'] + ' ' + df['Pincode']

        #Delivery person tags
        dl1 = ['babu','chandru', 'srinivas', 'gg', 'nandha','lokesh', 'madhu','prashanth','murugan','sandeep']
        l = []
        for x in df['tags']:
            y = x.split(',')
            l1 = []
            for z in y:
                if z.strip() in dl1:
                    l1.append(z.strip())

            l.append(l1)
        l = [', '.join(x) for x in l]
        df['Route'] = l

        #Carry bags
        l = []
        for item, order in zip(df['shipping_lines'], df['Order ID']):
            l1 = [order]
            for it in item:
                if "with carry bag" in it.title:
                    l1.append(", Carry Bag")
            if len(l1) == 1:
                l1.append("")
            l.append(l1)

        df = pd.merge(df, pd.DataFrame(l, columns=['Order ID','Carry Bag']), on='Order ID', how='left')
        df.drop(['shipping_lines','shipping_address','tags'], axis=1)
        return df
