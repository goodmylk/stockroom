from django.contrib import admin
from .models import Warehouse, WarehouseStock
# Register your models here.

admin.site.register(Warehouse)
admin.site.register(WarehouseStock)
