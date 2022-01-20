from .models import Warehouse

def all_warehouse(request):
    return {'all_warehouse': Warehouse.objects.all()}
