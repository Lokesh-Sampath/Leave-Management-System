from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer, TeamMemberSerializer, AdminUserListSerializer
from .permissions import IsManager, IsAdmin

class UserMeAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
    
class TeamMembersAPI(APIView):
    
    permission_classes = [IsManager]    
    
    def get(self, request):
        team = request.user.team_members.all()
        serializers = TeamMemberSerializer(team, many=True)
        return Response(serializers.data)
    
    
class AdminUserListAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserListSerializer(users, many=True)
        return Response(serializer.data)    