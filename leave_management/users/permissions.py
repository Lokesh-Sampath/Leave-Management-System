from rest_framework.permissions import BasePermission

class IsEmployee(BasePermission):
    
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and 
            request.user.userprofile.role == 'EMPLOYEE'
            )
        
        
class IsManager(BasePermission):
    
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            request.user.userprofile.role == 'MANAGER'
        )
        
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
                    