from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer

class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(sel,request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)