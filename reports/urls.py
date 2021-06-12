from django.urls import path
from . import views

urlpatterns = [
    path('instock/', views.instock, name = 'instock'),
    path('delivery/', views.delivery, name = 'delivery'),
    path('ndr/', views.notdelivered, name = 'notdelivered'),
    path('return/', views.returnreports, name = 'returnreports'),
]
