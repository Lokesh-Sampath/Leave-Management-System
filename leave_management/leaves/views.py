from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from users.permissions import IsEmployee
from rest_framework.views import APIView
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from rest_framework.response import Response
from rest_framework import status 
# Create your views here.

class EmployeeLeaveAPI(APIView):
     permission_classes = [IsAuthenticated, IsEmployee]
     
     def get(self, request):
         leaves = LeaveRequest.objects.filter(employee = request.user)
         serializer = LeaveRequestSerializer(leaves, many=True)
         return Response(serializer.data)
     
     def post(self, request):
          serializer = LeaveRequestSerializer(data = request.data)
          if serializer.is_valid():
              serializer.save(
                  employee = request.user,
                  status = "PENDING"
              )
              
              return Response(serializer.data, status = status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    