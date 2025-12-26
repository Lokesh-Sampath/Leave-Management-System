from django.urls import path
from .admin_views import  AdminUserListAPI

urlpatterns = [
    path('users/', AdminUserListAPI.as_view(), name='admin-users'),

]
