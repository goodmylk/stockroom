
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/', include('reports.urls'), name='reports'),
    path('products/', include('products.urls'), name='products'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('', include('dashboard.urls'))
]
