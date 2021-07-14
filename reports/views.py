
from django.shortcuts import render, redirect
import csv, io
from django.contrib.auth.decorators import login_required
from products.models import Product, Batch
from warehouse.models import Warehouse, WarehouseStock
from .models import Instock, Delivery, Notdelivered, Returnreports
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.db.models import F

#variables
warhouses = Warehouse.objects

#Views
@login_required(login_url="/accounts/login")
def instock(request):
    if request.method == 'POST':
        ct = request.POST['city']
        dt = request.POST['date']
        if dt and ct and type:

            if request.method == "GET":
                return render(request, 'reports/instock.html', {'warhouses':warhouses})

            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')

            data_set = csv_file.read().decode('UTF-8')

            io_string = io.StringIO(data_set)
            next(io_string)

            not_added = []
            msg = {}
            err = []
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                bch = column[1]
                qnt = column[2]
                if int(qnt) > 0:
                    try:
                        obj, created = WarehouseStock.objects.get_or_create(
                            name = Warehouse.objects.get(id= ct),
                            batch = Batch.objects.get(batch_number= bch),
                            defaults={"current_stock": qnt},
                            )

                        if not created:
                            WarehouseStock.objects.filter(name = Warehouse.objects.get(id= ct),
                            batch = Batch.objects.get(batch_number= bch)).update(current_stock=F("current_stock") + qnt)


                            ws = WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                            ).get(name = Warehouse.objects.get(pk = ct)).current_stock

                            if ws > 0:
                                WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                                ).filter(name = Warehouse.objects.get(pk = ct)).update(is_active = True)

                        add_ir = Instock()
                        add_ir.delivery_date = dt
                        add_ir.warehouse_name = Warehouse.objects.get(id= ct)
                        add_ir.submitted_by = request.user
                        add_ir.batch_number = Batch.objects.get(batch_number= bch)
                        add_ir.quantity = qnt
                        add_ir.save()

                    except Exception as e:
                        not_added.append(column[1])
                        err.append(e)

            if len(not_added) > 0:
                if len(not_added) == 1:
                    msg['message'] = f'{not_added[0]} batch is not saved.'
                else:
                    s = ','.join(not_added)
                    msg['message'] = f'{s} batches are not saved.'

                return render(request, 'reports/instock.html', {'message1':msg,'error':err, 'warhouses':warhouses})
            else:
                msg['message'] = 'Instock saved successfully.'
                return render(request, 'reports/instock.html', {'message':msg, 'warhouses':warhouses})
        else:
            return render(request, 'reports/instock.html', {'error':'Date and City are required.','warhouses':warhouses})
    else:
        return render(request, 'reports/instock.html', {'warhouses':warhouses})

@login_required(login_url="/accounts/login")
def delivery(request):
    if request.method == 'POST':
        ct = request.POST['city']
        dt = request.POST['date']
        type = request.POST['type']
        if dt and ct and type:

            if request.method == "GET":
                return render(request, 'reports/delivery.html', {'warhouses':warhouses})

            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')

            data_set = csv_file.read().decode('UTF-8')

            io_string = io.StringIO(data_set)
            next(io_string)

            not_added = []
            msg = {}
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                bch = column[1]
                qnt = column[2]
                if int(qnt) > 0:
                    if Batch.objects.filter(batch_number = bch).exists() and WarehouseStock.objects.filter(batch =  Batch.objects.get(batch_number=bch)).filter(name = Warehouse.objects.get(pk = ct)).exists():
                        
                        Batch.objects.filter(batch_number = bch).update(current_stock = F('current_stock') - qnt)
                        cs = Batch.objects.get(batch_number = bch).current_stock
                        if cs <= 0:
                            Batch.objects.filter(batch_number = bch).update(is_active = False)

                        WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                        ).filter(name = Warehouse.objects.get(pk = ct)
                        ).update(current_stock = F('current_stock') - qnt)

                        ws = WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                        ).get(name = Warehouse.objects.get(pk = ct)).current_stock
                        if ws <= 0:
                            WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                            ).filter(name = Warehouse.objects.get(pk = ct)).update(is_active = False)

                        dl = Delivery()
                        dl.delivery_date = dt
                        dl.quantity = qnt
                        dl.batch_number = Batch.objects.get(batch_number = bch)
                        dl.warehouse_name = Warehouse.objects.get(id= ct)
                        dl.submitted_by = request.user
                        dl.type = type
                        dl.save()

                    else:
                        not_added.append(column[1])

            if len(not_added) > 0:
                if len(not_added) == 1:
                    msg['message'] = f'{not_added[0]} batch is not saved.'
                else:
                    s = ','.join(not_added)
                    msg['message'] = f'{s} batches are not saved.'

                return render(request, 'reports/delivery.html', {'message1':msg, 'warhouses':warhouses})
            else:
                msg['message'] = 'Delivery report saved successfully.'
                return render(request, 'reports/delivery.html', {'message':msg, 'warhouses':warhouses})
        else:
            return render(request, 'reports/delivery.html', {'error':'Date, Type and City are required.', 'warhouses':warhouses})
    else:
        return render(request, 'reports/delivery.html', {'warhouses':warhouses})


@login_required(login_url="/accounts/login")
def notdelivered(request):
    if request.method == 'POST':

        ct = request.POST['city']
        dt = request.POST['date']

        if dt and ct:

            if request.method == "GET":
                return render(request, 'reports/notdelivered.html', {'warhouses':warhouses})

            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')

            data_set = csv_file.read().decode('UTF-8')

            io_string = io.StringIO(data_set)
            next(io_string)

            not_added = []
            err = []
            msg = {}

            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                bch = column[1]
                qnt = column[2]
                reason = column[3]
                order_id = column[4]

                if int(qnt) > 0:
                    try:
                        add_ndr = Notdelivered()
                        add_ndr.delivery_date = dt
                        add_ndr.order_id = order_id
                        add_ndr.reason = reason
                        add_ndr.warehouse_name = Warehouse.objects.get(id= ct)
                        add_ndr.submitted_by = request.user
                        add_ndr.batch_number = Batch.objects.get(batch_number= bch)
                        add_ndr.quantity = qnt
                        add_ndr.save()

                    except Exception as e:
                        not_added.append(column[1])
                        err.append(e)

            if len(not_added) > 0:
                if len(not_added) == 1:
                    msg['message'] = f'{not_added[0]} batch is not saved.'
                else:
                    s = ','.join(not_added)
                    msg['message'] = f'{s} batches are not saved.'

                return render(request, 'reports/notdelivered.html', {'message1':msg, 'error':err, 'warhouses':warhouses})
            else:
                msg['message'] = 'Delivery report saved successfully.'
                return render(request, 'reports/notdelivered.html', {'message':msg, 'warhouses':warhouses})
        else:
            return render(request, 'reports/notdelivered.html', {'error':'Date and City are required.', 'warhouses':warhouses})
    else:
        return render(request, 'reports/notdelivered.html', {'warhouses':warhouses})

@login_required(login_url="/accounts/login")
def returnreports(request):
    if request.method == 'POST':
        ct = request.POST['city']
        dt = request.POST['date']
        type = request.POST['type']
        if dt and ct and type:

            if request.method == "GET":
                return render(request, 'reports/returnreports.html', {'warhouses':warhouses})

            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'THIS IS NOT A CSV FILE')

            data_set = csv_file.read().decode('UTF-8')

            io_string = io.StringIO(data_set)
            next(io_string)

            not_added = []
            err = []
            msg = {}

            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                bch = column[1]
                qnt = column[2]

                if int(qnt) > 0:
                    if Batch.objects.filter(batch_number = bch).exists() and WarehouseStock.objects.filter(batch =  Batch.objects.get(batch_number=bch)).filter(name = Warehouse.objects.get(pk = ct)).exists():
                        Batch.objects.filter(batch_number = bch).update(current_stock = F('current_stock') + qnt)
                        cs = Batch.objects.get(batch_number = bch).current_stock
                        if cs > 0:
                            Batch.objects.filter(batch_number = bch).update(is_active = True)

                        WarehouseStock.objects.filter(batch =  Batch.objects.get(batch_number=bch)
                        ).filter(name = Warehouse.objects.get(pk = ct)
                        ).update(current_stock = F('current_stock') + qnt)

                        ws = WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                        ).get(name = Warehouse.objects.get(pk = ct)).current_stock
                        if ws > 0:
                            WarehouseStock.objects.filter(batch = Batch.objects.get(batch_number = bch)
                            ).filter(name = Warehouse.objects.get(pk = ct)).update(is_active = True)

                        add_dr = Returnreports()
                        add_dr.delivery_date = dt
                        add_dr.type = type
                        add_dr.warehouse_name = Warehouse.objects.get(id= ct)
                        add_dr.submitted_by = request.user
                        add_dr.batch_number = Batch.objects.get(batch_number= bch)
                        add_dr.quantity = qnt
                        add_dr.save()

                    else:
                        not_added.append(bch)

            if len(not_added) > 0:
                if len(not_added) == 1:
                    msg['message'] = f'{not_added[0]} batch is not saved.'
                else:
                    s = ','.join(not_added)
                    msg['message'] = f'{s} batches are not saved.'

                return render(request, 'reports/returnreports.html', {'message1':msg, 'warhouses':warhouses})
            else:
                msg['message'] = 'Return report saved successfully.'
                return render(request, 'reports/returnreports.html', {'message':msg, 'warhouses':warhouses})
        else:
            return render(request, 'reports/returnreports.html', {'error':'Date, Type and City are required.', 'warhouses':warhouses})
    else:
        return render(request, 'reports/returnreports.html', {'warhouses':warhouses})
