from django.urls import path
from .views import UserMeAPI, TeamMembersAPI

urlpatterns = [
    path('me/', UserMeAPI.as_view(), name='user-me'),
    path('team/',TeamMembersAPI.as_view(), name='team-members'),
]
