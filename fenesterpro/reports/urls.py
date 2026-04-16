from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('project/<int:pk>/', views.hub, name='hub'),
    path('project/<int:pk>/quotation/', views.quotation_report, name='quotation'),
    path('project/<int:pk>/boq/', views.boq_report, name='boq'),
    path('project/<int:pk>/cutting/', views.cutting_report, name='cutting'),
    path('project/<int:pk>/excel/', views.excel_report, name='excel'),
]
