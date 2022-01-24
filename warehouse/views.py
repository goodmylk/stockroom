from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from products.models import Product, Batch
from .models import Warehouse, WarehouseStock
from django.db.models import Sum, Max, Q, Avg
from reports.models import Delivery
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from datetime import date, timedelta
import json
from django.http import HttpResponse
import csv

# Create your views here.
@login_required(login_url="/accounts/login")
def whouse(request, warehouse_id):
    wh = get_object_or_404(Warehouse, pk=warehouse_id)

    batch = (WarehouseStock.objects
    .filter(is_active = True)
    .filter(name = Warehouse.objects.get(pk = warehouse_id))
    .values('batch__productname')
    .annotate(dcount=Sum('current_stock'))
    .order_by()
    )

    weekly_average = list((Delivery.objects
    .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
    .filter(~Q(type="ST"))
    .annotate(week=ExtractWeek('delivery_date'))
    .values('week','batch_number__productname')
    .annotate(sum_quantity=Sum('quantity'))
    .values('batch_number__productname','sum_quantity')
    ))

    wk_avg = {}
    for q in weekly_average:
        k = q['batch_number__productname']
        wk_avg.setdefault(k, [])
        wk_avg[k].append(q['sum_quantity'])

    for l in batch:
        name = Product.objects.get(pk=l["batch__productname"])
        l['name'] = name
        try:
            l['wk_avg'] = sum(wk_avg[l["batch__productname"]])/len(wk_avg[l["batch__productname"]])
        except KeyError:
            l['wk_avg'] = ''

    update = Delivery.objects.filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id)).aggregate(dcount=Max('delivery_date'))

    ty1 = Delivery.objects.filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id)).filter(~Q(type="ST")).values("type").distinct()
    ty = ["All"]
    for t in ty1:
        ty.append(t['type'])

    select_date = ["This_Week","This_Month","Last_Week","Last_Month"]
    current_year = timezone.now().year
    current_week = date.today().isocalendar()[1]
    current_month = timezone.now().month

    if request.method == 'POST':

        tm = request.POST['time']
        select_date.remove(tm)
        select_date.insert(0, tm)

        typ = request.POST['type']
        ty.remove(typ)
        ty.insert(0, typ)

        if typ == "All":
            if (tm == "This_Week") | (tm == "Last_Week"):

                if tm == "Last_Week":
                    wk = timezone.now() - timedelta(days=7)
                    current_week = wk.isocalendar()[1]
                    current_year = wk.year

                volume = (Delivery.objects
                .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
                .filter(delivery_date__year=current_year)
                .filter(delivery_date__week=current_week)
                .filter(~Q(type="ST"))
                .values('batch_number__productname')
                .annotate(sum_quantity=Sum('quantity'))
                .order_by()
                )

                for l in volume:
                    name = Product.objects.get(pk=l["batch_number__productname"])
                    l['name'] = str(name)

                return render(request, 'warehouse.html', {'warehouse':wh,'batches':batch,'update':update,
                    "select_date":select_date,"ty":ty,'volume':volume})

            else:
                if (tm == "Last_Month"):
                    mon = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
                    current_month = mon.month
                    current_year = mon.year

                volume = (Delivery.objects
                .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
                .filter(delivery_date__year=current_year)
                .filter(delivery_date__month=current_month)
                .filter(~Q(type="ST"))
                .values('batch_number__productname')
                .annotate(sum_quantity=Sum('quantity'))
                .order_by()
                )

                for l in volume:
                    name = Product.objects.get(pk=l["batch_number__productname"])
                    l['name'] = str(name)

                return render(request, 'warehouse.html', {'warehouse':wh,'batches':batch,'update':update,
                    "select_date":select_date,"ty":ty,'volume':volume})

        else:

            if (tm == "This_Week") | (tm == "Last_Week"):

                if tm == "Last_Week":
                    wk = timezone.now() - timedelta(days=7)
                    current_week = wk.isocalendar()[1]
                    current_year = wk.year

                volume = (Delivery.objects
                .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
                .filter(delivery_date__year=current_year)
                .filter(delivery_date__week=current_week)
                .filter(type=typ)
                .values('batch_number__productname')
                .annotate(sum_quantity=Sum('quantity'))
                .order_by()
                )

                for l in volume:
                    name = Product.objects.get(pk=l["batch_number__productname"])
                    l['name'] = str(name)

                return render(request, 'warehouse.html', {'warehouse':wh,'batches':batch,'update':update,
                    "select_date":select_date,"ty":ty,'volume':volume})

            else:
                if (tm == "Last_Month"):
                    mon = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
                    current_month = mon.month
                    current_year = mon.year

                volume = (Delivery.objects
                .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
                .filter(delivery_date__year=current_year)
                .filter(delivery_date__month=current_month)
                .filter(type=typ)
                .values('batch_number__productname')
                .annotate(sum_quantity=Sum('quantity'))
                .order_by()
                )

                for l in volume:
                    name = Product.objects.get(pk=l["batch_number__productname"])
                    l['name'] = str(name)

                return render(request, 'warehouse.html', {'warehouse':wh,'batches':batch,'update':update,
                    "select_date":select_date,"ty":ty,'volume':volume})

    else:

        volume = (Delivery.objects
        .filter(warehouse_name = Warehouse.objects.get(pk = warehouse_id))
        .filter(delivery_date__year=current_year)
        .filter(delivery_date__week=current_week)
        .filter(~Q(type="ST"))
        .values('batch_number__productname')
        .annotate(sum_quantity=Sum('quantity'))
        .order_by()
        )

        for l in volume:
            name = Product.objects.get(pk=l["batch_number__productname"])
            l['name'] = str(name)



        return render(request, 'warehouse.html', {'warehouse':wh,'batches':batch,'update':update,'volume':volume,
                        "select_date":select_date, "ty":ty})
