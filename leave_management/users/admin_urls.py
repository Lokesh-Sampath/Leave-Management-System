from django.urls import path
from .admin_views import  AdminUserListAPI, AdminUserUpdateAPIView, LeaveBalanceUpdateAPI

urlpatterns = [
    path('users/', AdminUserListAPI.as_view(), name='admin-users'),
    path('users/<int:id>/', AdminUserUpdateAPIView.as_view()),
    path('leave-balances/<int:user_id>/', LeaveBalanceUpdateAPI.as_view()),


]
