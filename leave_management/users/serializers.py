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