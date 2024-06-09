from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import *

class HasApplicantPaid(BasePermission):

    def has_permission(self, request, view):
        if hasattr(request.user, "applicant"):
            applicant = request.user.applicant
            post_pk = view.kwargs.get("post_pk")
            post = Post.objects.get(id=post_pk)
            if not post.is_paid:
                return True
            
            try:
                PaidApplicant.objects.get(applicant=applicant, post_id=post_pk)
                return True
            except PaidApplicant.DoesNotExist:
                return False 
            
class PostPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, "organization"):
            return True
        if request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return True
        return False