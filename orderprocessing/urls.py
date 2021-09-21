from django.urls import path
from . import views

urlpatterns = [
    path('bengaluru', views.bengaluru, name = 'bengaluru'),
]
