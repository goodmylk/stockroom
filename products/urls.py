from django.urls import path
from . import views

urlpatterns = [
    path('addbatch', views.addbatch, name = 'addbatch'),
]
