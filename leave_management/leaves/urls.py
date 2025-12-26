from django.urls import path
from .views import EmployeeLeaveAPI, LeaveDetailedAPI, TeamLeaveAPI

urlpatterns = [
    path('',EmployeeLeaveAPI.as_view()),
    path("<int:leave_id>/", LeaveDetailedAPI.as_view(), name='employee-leave'),
    path('team/', TeamLeaveAPI.as_view(), name='team-leaves'),
]
