from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer, TeamMemberSerializer
from .permissions import IsManager

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