
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product, Batch
from warehouse.models import Warehouse
from .models import Instock, Delivery, Notdelivered, Returnreports
from django.utils import timezone
from django.views.decorators.cache import never_cache

#variables
def get_updated_data():
    d = {}
    pr = Product.objects
    bt = Batch.objects
    for x in list(pr.values_list('id', flat=True)):
        name = list(pr.values_list('productname', flat=True).filter(pk = x))
        y = list(bt.values_list('batch_number', flat=True).filter(productname = x))
        if len(y) > 0:
            d[name[0]] = [str(z) for z in y]
    return d

warhouses = Warehouse.objects

reason_list = ["Address not found","Phone not reachable/switched off","Customer canceled the order/put on hold",
                "Too many orders in a particular route", "Stocks not available","Delivery person not available in the warehouse"]

#Views
@login_required(login_url="/accounts/login")
@never_cache
def instock(request):
    if request.method == 'POST':
        if request.POST['date'] and request.POST['city']:
            for k in d.keys():
                if request.POST[f'qnt {k}'] and request.POST[f'batch {k}']:
                    add_ir = Instock()
                    add_ir.delivery_date = request.POST['date']
                    add_ir.warehouse_name = Warehouse.objects.get(id= request.POST['city'])
                    add_ir.submitted_by = request.user
                    add_ir.batch_number = Batch.objects.get(batch_number= request.POST[f'batch {k}'])
                    add_ir.quantity = request.POST[f'qnt {k}']
                    add_ir.submission_date = timezone.datetime.now()
                    if request.POST['comments']:
                    	add_ir.comments = request.POST['comments']

                    add_ir.save()
            return redirect('/')
        else:
            d = get_updated_data()
            return render(request, 'reports/instock.html', {'error':'Date and City are required.','batches': d, 'warhouses':warhouses})
    else:
        d = get_updated_data()
        return render(request, 'reports/instock.html', {'batches': d, 'warhouses':warhouses})

@login_required(login_url="/accounts/login")
@never_cache
def delivery(request):
    if request.method == 'POST':
        if request.POST['date'] and request.POST['city'] and request.POST['type']:
            for k in d.keys():
                if request.POST[f'qnt {k}'] and request.POST[f'batch {k}']:
                    add_dr = Delivery()
                    add_dr.delivery_date = request.POST['date']
                    add_dr.type = request.POST['type']
                    add_dr.warehouse_name = Warehouse.objects.get(id= request.POST['city'])
                    add_dr.submitted_by = request.user
                    add_dr.batch_number = Batch.objects.get(batch_number= request.POST[f'batch {k}'])
                    add_dr.quantity = request.POST[f'qnt {k}']
                    add_dr.submission_date = timezone.datetime.now()
                    if request.POST['comments']:
                    	add_dr.comments = request.POST['comments']

                    add_dr.save()
            return redirect('/')
        else:
            d = get_updated_data()
            return render(request, 'reports/delivery.html', {'error':'Date, Type and City are required.','batches': d, 'warhouses':warhouses})
    else:
        d = get_updated_data()
        return render(request, 'reports/delivery.html', {'batches': d, 'warhouses':warhouses})


@login_required(login_url="/accounts/login")
@never_cache
def notdelivered(request):
    if request.method == 'POST':
        if request.POST['date'] and request.POST['orderid'] and request.POST['reason'] and request.POST['city']:
            for k in d.keys():
                if request.POST[f'qnt {k}'] and request.POST[f'batch {k}']:
                    add_ndr = Notdelivered()
                    add_ndr.delivery_date = request.POST['date']
                    add_ndr.order_id = request.POST['orderid']
                    add_ndr.reason = request.POST['reason']
                    add_ndr.warehouse_name = Warehouse.objects.get(id= request.POST['city'])
                    add_ndr.submitted_by = request.user
                    add_ndr.batch_number = Batch.objects.get(batch_number= request.POST[f'batch {k}'])
                    add_ndr.quantity = request.POST[f'qnt {k}']
                    if request.POST['comments']:
                    	add_ndr.comments = request.POST['comments']
                    add_ndr.save()

            return redirect('/')
        else:
            d = get_updated_data()
            return render(request, 'reports/notdelivered.html', {'error':'Date, Order ID, Reason and City are required.','batches': d, 'reasons':reason_list, 'warhouses':warhouses})
    else:
        d = get_updated_data()
        return render(request, 'reports/notdelivered.html', {'batches': d, 'reasons':reason_list, 'warhouses':warhouses})

@login_required(login_url="/accounts/login")
@never_cache
def returnreports(request):
    if request.method == 'POST':
        if request.POST['date'] and request.POST['city'] and request.POST['type']:
            for k in d.keys():
                if request.POST[f'qnt {k}'] and request.POST[f'batch {k}']:
                    add_dr = Returnreports()
                    add_dr.delivery_date = request.POST['date']
                    add_dr.type = request.POST['type']
                    add_dr.warehouse_name = Warehouse.objects.get(id= request.POST['city'])
                    add_dr.submitted_by = request.user
                    add_dr.batch_number = Batch.objects.get(batch_number= request.POST[f'batch {k}'])
                    add_dr.quantity = request.POST[f'qnt {k}']
                    add_dr.submission_date = timezone.datetime.now()
                    if request.POST['comments']:
                    	add_dr.comments = request.POST['comments']

                    add_dr.save()

            return redirect('/')
        else:
            d = get_updated_data()
            return render(request, 'reports/returnreports.html', {'error':'Date, Type and City are required.','batches': d, 'warhouses':warhouses})

    else:
        d = get_updated_data()
        return render(request, 'reports/returnreports.html', {'batches': d, 'warhouses':warhouses})
