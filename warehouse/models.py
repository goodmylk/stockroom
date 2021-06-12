from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name
