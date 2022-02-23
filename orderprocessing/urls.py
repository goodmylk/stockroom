from django.urls import path
from . import views

urlpatterns = [
    path('nationwide', views.nationwide, name = 'nationwide'),
    path('amazon', views.amazon, name = 'amazon'),
    path('orderwebhook', views.orderwebhook, name = 'orderwebhook'),
]
