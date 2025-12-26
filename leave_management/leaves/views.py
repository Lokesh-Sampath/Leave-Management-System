from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsEmployee
from rest_framework.views import APIView
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, TeamLeaveSerializer, LeaveActionSerializer
from rest_framework.response import Response
from rest_framework import status 
from users.permissions import IsManager
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
    
    
class TeamLeaveAPI(APIView):
    
    permission_classes = [IsAuthenticated,IsManager]  
    
    def get(self,request):
        
        team_profiles = request.user.team_members.all()  
        team_users = [profile.user for profile in team_profiles]
        
        leaves = LeaveRequest.objects.filter(
            employee__in = team_users,
            status = 'PENDING'
        )
        
        serializer = LeaveRequestSerializer(leaves, many=True)
        
        return Response(serializer.data)
    
    
class LeaveActionAPI(APIView):
    
    permission_classes = [IsAuthenticated,IsManager]
    
    def patch(self, request, leave_id):
        
       try:
           leave = LeaveRequest.objects.get(id = leave_id)    
       except  LeaveRequest.DoesNotExist:
               return Response(
             {'details' : "User donsen't exist "},
               status = status.HTTP_404_NOT_FOUND
           )   
               
       if leave.employee.userprofile.manager != request.user:
            return Response(
                {'details' : "Yu are not authorized to act on this action"},
                status= status.HTTP_403_FORBIDDEN
            )
            
       if leave.status != 'PENDING':
           return Response(
               {'details':"The required act has been alreay took over"},
               status = status.HTTP_400_BAD_REQUEST
           ) 
           
           
       serializer = LeaveActionSerializer(data = request.data)
       serializer.is_valid(raise_exception = True)
       
       action = serializer.validated_data['action']
       
       if action == 'APPROVE':
           leave.status = "APPROVED"
           leave.aproved_by = request.user
           leave.rejection_reason = None
           
       elif action == 'REJECT':
           leave.status = 'REJECTED'
           leave.approved_by = request.user
           leave.rejection_reason = serializer.validated_data.get(
                'rejection_reason', ''
            )
           
       leave.save()   
       
       
       return Response(
           {'status':leave.status},
           status = status.HTTP_200_OK
                        )