from django.urls import path
from .admin_views import  AdminUserListAPI, AdminUserUpdateAPIView

urlpatterns = [
    path('users/', AdminUserListAPI.as_view(), name='admin-users'),
    path('users/<int:id>/', AdminUserUpdateAPIView.as_view()),

]
