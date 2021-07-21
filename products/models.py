from django.db import models
from django.contrib.auth.models import User

def get_deleted_user_instance():
    return User.objects.get(username='deleted')

# Create your models here.
class Product(models.Model):
    productname = models.CharField(max_length=100)
    is_active = models.BooleanField()
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.productname


class Batch(models.Model):
    batch_number = models.CharField(max_length = 50)
    productname = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    manufacture_date = models.DateTimeField()
    quantity = models.IntegerField()
    comments = models.TextField(null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET(get_deleted_user_instance))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.batch_number +"_"+ self.productname.productname

    def date_pretty(self):
        return self.manufacture_date.strftime('%b %e %Y')

    def batch_list(self, pk):
        if self.productname == pk:
            return self.batch_number
