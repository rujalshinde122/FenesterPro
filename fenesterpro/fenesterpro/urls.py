from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('projects/', include('projects.urls')),
    path('calculator/', include('calculator.urls')),
    path('optimizer/', include('optimizer.urls')),
    path('reports/', include('reports.urls')),
]
