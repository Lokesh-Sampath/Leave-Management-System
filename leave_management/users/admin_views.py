from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer, TeamMemberSerializer, AdminUserListSerializer
from .permissions import IsManager, IsAdmin

class AdminUserListAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserListSerializer(users, many=True)
        return Response(serializer.data)    