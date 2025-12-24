from django.urls import path
from .views import EmployeeLeaveAPI

urlpatterns = [
    path('',EmployeeLeaveAPI.as_view())
]
