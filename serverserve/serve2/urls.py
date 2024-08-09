from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view_all_emp/', views.view_all_emp, name='view_all_emp'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('remove_emp/<int:emp_id>/', views.remove_emp, name='remove_emp'),
    path('remove_emp/', views.remove_emp, name='remove_emp'),
    path('filter_emp/', views.filter_emp, name='filter_emp'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('start-session/', views.start_session, name='start_session'),
    path('end-session/', views.end_session, name='end_session'),
]
