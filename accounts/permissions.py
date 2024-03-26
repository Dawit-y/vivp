from rest_framework.permissions import BasePermission

from .models import *

class IsApplicant(BasePermission):
 
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return isinstance(request.user, Applicant)
