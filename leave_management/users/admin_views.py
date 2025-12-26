from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer, TeamMemberSerializer, AdminUserListSerializer, AdminCreateUserSerializer
from .permissions import IsManager, IsAdmin

class AdminUserListAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all()
        serializer = AdminUserListSerializer(users, many=True)
        return Response(serializer.data)    
    
    
    def post(self, request):
        serializer = AdminCreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "user_id": user.id,
                    "status": "User created successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )