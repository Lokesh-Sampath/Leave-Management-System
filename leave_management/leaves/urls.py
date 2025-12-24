from django.urls import path
from .views import EmployeeLeaveAPI, LeaveDetailedAPI

urlpatterns = [
    path('',EmployeeLeaveAPI.as_view()),
    path("<int:leave_id>/", LeaveDetailedAPI.as_view()),
]
