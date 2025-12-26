from rest_framework import serializers
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'id',
            'leave_type',
            'start_date',
            'end_date',
            'reason',
            'status',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

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
    
    