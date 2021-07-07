from django.db import models
from products.models import Batch, Product

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class WarehouseStock(models.Model):
    name = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    batch = models.ForeignKey('products.Batch', on_delete=models.CASCADE)
    current_stock = models.IntegerField()
    last_updated = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name.name + "_" +self.batch.batch_number
