from django.db import models
from products.models import Batch
from warehouse.models import Warehouse
from django.contrib.auth.models import User

# Create your models here.
def get_deleted_user_instance():
    return User.objects.get(username='deleted')

class Returnreports(models.Model):

    delivery_date = models.DateTimeField()
    quantity = models.IntegerField()
    batch_number = models.ForeignKey('products.Batch', on_delete=models.CASCADE)
    warehouse_name = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance))
    type = models.CharField(max_length = 10)
    submission_date = models.DateTimeField()

    def __str__(self):
        return str(self.delivery_date.strftime('%b %e %Y'))

class Notdelivered(models.Model):

    delivery_date = models.DateTimeField()
    order_id = models.IntegerField()
    quantity = models.IntegerField()
    reason = models.CharField(max_length = 50)
    batch_number = models.ForeignKey('products.Batch', on_delete=models.CASCADE)
    warehouse_name = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance))
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.order_id)

class Instock(models.Model):

    delivery_date = models.DateTimeField()
    quantity = models.IntegerField()
    batch_number = models.ForeignKey('products.Batch', on_delete=models.CASCADE)
    warehouse_name = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance))
    submission_date = models.DateTimeField()

    def __str__(self):
        return str(self.delivery_date.strftime('%b %e %Y'))

class Delivery(models.Model):

    delivery_date = models.DateTimeField()
    quantity = models.IntegerField()
    batch_number = models.ForeignKey('products.Batch', on_delete=models.CASCADE)
    warehouse_name = models.ForeignKey('warehouse.Warehouse', on_delete=models.CASCADE)
    comments = models.TextField(null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance))
    type = models.CharField(max_length = 10)
    submission_date = models.DateTimeField()

    def __str__(self):
        return str(self.delivery_date.strftime('%b %e %Y'))
