from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Batch, Product
from reports.models import Delivery
from django.db.models import Sum, Max
from warehouse.models import Warehouse, WarehouseStock

# Create your views here.
@login_required(login_url="/accounts/login")
def home(request):
    warehousestocks = WarehouseStock.objects.filter(is_active = True).order_by('batch__productname__productname','batch__manufacture_date')
    update = (Delivery.objects
              .values('warehouse_name__name')
              .annotate(dcount=Max('delivery_date'))
              .order_by()
              )
    if request.method == 'POST':
        if request.POST['city'] == "Overall":

            batch = (WarehouseStock.objects
            .filter(is_active = True)
            .values('batch__productname__productname')
            .annotate(dcount=Sum('current_stock'))
            .order_by('batch__productname__productname','-dcount')
            )

            warehouse = Warehouse.objects
            wh = ["Overall"]
            for x in list(warehouse.values_list('name', flat=True)):
                wh.append(x)


            return render(request, 'home/dashboard.html', {'batches': batch, 'warehouses':wh, 'warehousestocks':warehousestocks, 'update':update})
        else:
            warehouse = Warehouse.objects

            wh = [request.POST['city'], "Overall"]
            for x in list(warehouse.values_list('name', flat=True)):
                if x != request.POST['city']:
                    wh.append(x)

            batch = (WarehouseStock.objects
            .filter(is_active = True)
            .filter(name = Warehouse.objects.get(name = request.POST['city']))
            .values('batch__productname__productname')
            .annotate(dcount=Sum('current_stock'))
            .order_by('batch__productname__productname','-dcount')
            )

            return render(request, 'home/dashboard.html', {'warehouses':wh, 'batches': batch, 'warehousestocks':warehousestocks, 'update':update})

    else:
        batch = (WarehouseStock.objects
        .filter(is_active = True)
        .values('batch__productname__productname')
        .annotate(dcount=Sum('current_stock'))
        .order_by('batch__productname__productname','-dcount')
        )
        warehouse = Warehouse.objects
        wh = ["Overall"]
        for x in list(warehouse.values_list('name', flat=True)):
            wh.append(x)

        return render(request, 'home/dashboard.html', {'batches': batch, 'warehouses':wh, 'warehousestocks':warehousestocks, 'update':update})
