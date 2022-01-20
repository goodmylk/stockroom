from django.urls import path
from . import views

urlpatterns = [
    path('<int:warehouse_id>', views.whouse, name = 'whouse'),
]
