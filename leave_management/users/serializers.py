from rest_framework import serializers
from django.contrib.auth.models import User


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source = "userprofile.role")
    manager = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields=  ['id','username','email','role','manager']
        
    
    def get_manager(self,obj):
        
        profile = obj.userprofile
        
        if profile.manager:
            return profile.manager.username
        return None    
    
from rest_framework import serializers
from .models import UserProfile

class TeamMemberSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email']


class AdminUserListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='userprofile.role')

    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        
class AdminCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['EMPLOYEE', 'MANAGER'])
    manager_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, data):
        role = data.get('role')
        manager_id = data.get('manager_id')

        if role == 'MANAGER' and manager_id:
            raise serializers.ValidationError(
                "Manager cannot have a manager assigned"
            )

        if role == 'EMPLOYEE' and manager_id:
            if not UserProfile.objects.filter(
                user_id=manager_id,
                role='MANAGER'
            ).exists():
                raise serializers.ValidationError(
                    "manager_id must belong to a manager"
                )

        return data

    def create(self, validated_data):
     password = validated_data.pop("password")
     role = validated_data.pop("role", None)
     manager_id = validated_data.pop("manager_id", None)

     user = User.objects.create_user(
        password=password,
        **validated_data
     )

     profile = user.userprofile

     if role:
        profile.role = role

     if manager_id:
        profile.manager = User.objects.get(id=manager_id)

     profile.save()
     return user

        
class AdminUserUpdateSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=['EMPLOYEE', 'MANAGER'],
        required=False
    )
    manager_id = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
     profile, created = UserProfile.objects.get_or_create(user=instance)

     if 'role' in validated_data:
        profile.role = validated_data['role']

     if 'manager_id' in validated_data:
        manager_id = validated_data['manager_id']

        if manager_id is None:
            profile.manager = None
        else:
            profile.manager = User.objects.get(id=manager_id)

     profile.save()
     return instance