
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/', include('reports.urls'), name='reports'),
    path('slackbot/', include('slackbot.urls'), name='slackbot'),
    path('products/', include('products.urls'), name='products'),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('warehouse/', include('warehouse.urls'), name='warehouse'),
    path('orderprocessing/', include('orderprocessing.urls'), name='orderprocessing'),
    path('shopify/', include('shopify_app.urls')),
    path('', include('dashboard.urls'))
]
