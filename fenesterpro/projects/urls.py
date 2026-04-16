from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('new/', views.project_create, name='new'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('<int:pk>/add-window/', views.add_window, name='add_window'),
    path('<int:pk>/calculate/', views.calculate_project, name='calculate'),
    path('<int:pk>/optimise/', views.optimise_project, name='optimise'),
]
