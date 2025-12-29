from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from users.serializers import UserMeSerializer, TeamMemberSerializer, AdminUserListSerializer, AdminCreateUserSerializer, AdminUserUpdateSerializer
from .permissions import IsManager, IsAdmin
from leaves.serializers import LeaveBalanceCreateSerializer

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
        
class AdminUserUpdateAPIView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminUserUpdateSerializer(
            instance=user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLeaveBalanceAPI(APIView):
    
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = LeaveBalanceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        balance = serializer.save()

        
        return Response(
            {
                "user_id": balance.user.id,
                "total_leaves": balance.total_leaves,
                "used_leaves": balance.used_leaves,
                "remaining_leaves": balance.remaining_leave()
            },
            status = status.HTTP_201_CREATED
        )    