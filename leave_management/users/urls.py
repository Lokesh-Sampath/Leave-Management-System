from django.urls import path
from .views import UserMeAPIView

urlpatterns = [
    path('me/', UserMeAPIView.as_view(), name='user-me'),
]
