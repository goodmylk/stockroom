from django.contrib import admin

from .models import Returnreports, Notdelivered, Instock, Delivery

# Register your models here.
admin.site.register(Returnreports)
admin.site.register(Notdelivered)
admin.site.register(Instock)
admin.site.register(Delivery)
