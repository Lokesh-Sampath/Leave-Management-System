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
      
      
      
class LeaveDetailedAPI(APIView):
    
    permission_classes = [IsAuthenticated, IsEmployee]
    
    def get(self, request,leave_id):
        
        try : 
            leave = LeaveRequest.objects.get(id = leave_id)
        except LeaveRequest.DoesNotExist:
            return Response(
                {"detail": "Leave not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if leave.employee != request.user:
            return Response(
                {"detail" : "Not Allowed"},
                status = status.HTTP_403_FORBIDDEN
            )    
              
        serializer  = LeaveRequestSerializer(leave)
        return Response(serializer.data)      