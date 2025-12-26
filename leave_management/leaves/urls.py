from django.urls import path
from .views import EmployeeLeaveAPI, LeaveDetailedAPI, TeamLeaveAPI, LeaveActionAPI

urlpatterns = [
    path('',EmployeeLeaveAPI.as_view()),
    path("<int:leave_id>/", LeaveDetailedAPI.as_view(), name='employee-leave'),
    path('team/', TeamLeaveAPI.as_view(), name='team-leaves'),
    path('<int:leave_id>/action/', LeaveActionAPI.as_view(), name='leave-action'),
]
