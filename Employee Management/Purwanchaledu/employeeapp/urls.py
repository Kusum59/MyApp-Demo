from django.urls import path
from .import views 

urlpatterns = [
   path('employee/create',views.EmployeeCreateApiView.as_view(), name = 'employee-create'), 
   path('employee/list', views.EmployeeListApiView.as_view(),name = 'employee-list'),
   path('employee/<pk>/edit', views.EmployeeEditApiView.as_view(),name = 'employee-edit'),
   path('employee/<pk>/delete', views.EmployeeDeleteApiView.as_view(),name = 'employee-delete')

]