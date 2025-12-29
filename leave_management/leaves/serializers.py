from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance
from django.contrib.auth.models import User

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(
        source="employee.username",
        read_only=True
    )

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "employee",
            "start_date",
            "end_date",
            "leave_type",
            "status",
            "created_at",
        ]


    def create(self, validated_data):
        return LeaveRequest.objects.create(**validated_data)


class TeamLeaveSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.username')
    
    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'employee',
            'leave_type',
            'start_date',
            'end_date',
            'status'
        ]
        
class LeaveActionSerializer(serializers.Serializer):
    
    action  = serializers.ChoiceField(choices = ['APPROVE','REJECT'])   
    rejection_reason = serializers.CharField(required=False, allow_blank=True) 
    
    
class LeaveBalanceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ["total_leaves", "used_leaves","remaining_leave"]
        extra_kwargs = {
            "total_leaves": {"required": False},
            "used_leaves": {"required": False},
        }
        
    def get_remaining_leave(self, obj):
        return obj.remaining_leave()

