from django.urls import path
from .views import UserMeAPI, TeamMembersAPI, AdminUserListAPI

urlpatterns = [
    path('me/', UserMeAPI.as_view(), name='user-me'),
    path('team/',TeamMembersAPI.as_view(), name='team-members'),
    path('admin/users/', AdminUserListAPI.as_view(), name='admin-users'),

]
