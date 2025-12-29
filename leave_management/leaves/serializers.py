from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance
from django.contrib.auth.models import User

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
    
    
class LeaveBalanceCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = LeaveBalance
        fields = ["user_id", "total_leaves"]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        total_leaves = validated_data["total_leaves"]

        user = User.objects.get(id=user_id)

        balance, created = LeaveBalance.objects.get_or_create(
            user=user,
            defaults={
                "total_leaves": total_leaves,
                "used_leaves": 0
            }
        )

        if not created:
            raise serializers.ValidationError(
                "Leave balance already exists for this user."
            )

        return balance
