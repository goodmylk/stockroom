from django.db import models

# Create your models here.
class Productsactive(models.Model):
    product_id = models.IntegerField()
    title = models.CharField(max_length = 50)
    cleansing_mylk = models.IntegerField(default=0)
    butter = models.IntegerField(default=0)
    after_shave_mylk = models.IntegerField(default=0)
    curd = models.IntegerField(default=0)
    mayo = models.IntegerField(default=0)
    mylk = models.IntegerField(default=0)
    mylk_1L_Pack = models.IntegerField(default=0)
    choc_mylk = models.IntegerField(default=0)
    no_sugar_mylk = models.IntegerField(default=0)
    no_sugar_mylk_1L_Pack = models.IntegerField(default=0)
    cheese = models.IntegerField(default=0)
    paneer = models.IntegerField(default=0)
    thunder = models.IntegerField(default=0)
    ranch = models.IntegerField(default=0)
    parmesan = models.IntegerField(default=0)
    shampoo_bar = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Amzonproducts(models.Model):
    sku = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)
    contents = models.CharField(max_length = 50)
    pack = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.title

class Box(models.Model):
    Box = models.CharField(max_length = 5)
    Height = models.FloatField()
    Length = models.FloatField()
    Width = models.FloatField()
    mylk = models.IntegerField(default=0)
    butter = models.IntegerField(default=0)
    mayo = models.IntegerField(default=0)

    def __str__(self):
        return self.Box
