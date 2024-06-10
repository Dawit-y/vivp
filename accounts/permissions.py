from rest_framework.permissions import BasePermission

from .models import *

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        
class IsSystemCoordinator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True

class IsApplicant(BasePermission):
 
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, "applicant")
    
class IsStudent(BasePermission):
 
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, "student")
    
class IsUniversityCoordinator(BasePermission):
 
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, "universitycoordinator")
    
class IsUniversitySupervisor(BasePermission):
 
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, "universitysupervisor")
    
class IsOrganization(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return hasattr(request.user, "organization")
