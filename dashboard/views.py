from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Batch, Product
from django.db.models import Sum, Max
from warehouse.models import Warehouse, WarehouseStock

# Create your views here.
@login_required(login_url="/accounts/login")
def home(request):
    warehousestocks = WarehouseStock.objects.filter(is_active = True)
    if request.method == 'POST':
        if request.POST['city'] == "Overall":
            batch = (Batch.objects
            .filter(is_active = True)
            .values('productname')
            .annotate(dcount=Sum('current_stock'),  max_date=Max('last_updated'))
            .order_by('productname')
            )
            warehouse = Warehouse.objects
            wh = ["Overall"]
            for x in list(warehouse.values_list('name', flat=True)):
                wh.append(x)
            for l in batch:
                 name = Product.objects.get(pk=l['productname'])
                 l['name'] = name
            return render(request, 'home/dashboard.html', {'batches': batch, 'warehouses':wh, 'warehousestocks':warehousestocks})
        else:
            warehouse = Warehouse.objects

            wh = [request.POST['city'], "Overall"]
            for x in list(warehouse.values_list('name', flat=True)):
                if x != request.POST['city']:
                    wh.append(x)

            batch = (WarehouseStock.objects
            .filter(is_active = True)
            .filter(name = Warehouse.objects.get(name = request.POST['city']))
            .values('batch__productname')
            .annotate(dcount=Sum('current_stock'),  max_date=Max('last_updated'))
            .order_by()
            )

            for l in batch:
                 name = Product.objects.get(pk=l["batch__productname"])
                 l['name'] = name

            return render(request, 'home/dashboard.html', {'warehouses':wh, 'batches': batch, 'warehousestocks':warehousestocks})

    else:
        batch = (Batch.objects
        .filter(is_active = True)
        .values('productname')
        .annotate(dcount=Sum('current_stock'),  max_date=Max('last_updated'))
        .order_by('productname')
        )
        warehouse = Warehouse.objects
        wh = ["Overall"]
        for x in list(warehouse.values_list('name', flat=True)):
            wh.append(x)
        for l in batch:
             name = Product.objects.get(pk=l['productname'])
             l['name'] = name
        return render(request, 'home/dashboard.html', {'batches': batch, 'warehouses':wh, 'warehousestocks':warehousestocks})
