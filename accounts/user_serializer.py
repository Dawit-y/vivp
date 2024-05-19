from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','password', 'email', 'first_name', 'last_name','phone_number',"avatar", "is_staff"]
    
class UserSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField(method_name="get_role")
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', "role"]
        ref_name = "user_serializer"

    def get_role(self, obj):
        if obj.is_superuser:
            return "admin"
        if obj.is_staff:
            return "system_coordinator"
        if hasattr(obj, "applicant"):
            if hasattr(obj.applicant, "student"):
                return "student"
            return "applicant"
        if hasattr(obj, "organization"):
            return "organization"
        if hasattr(obj, "universitycoordinator"):
            return "university_coordinator"
        if hasattr(obj, "universitysupervisor"):
            return "university_supervisor"
        return "unknown"



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        serializer = UserSerializer(user)
        token["role"] = serializer.data["role"]

        if user.is_superuser:
            token["admin_id"] = user.id
        if user.is_staff:
            token["system_coordinator_id"] = user.id
        if hasattr(user, "applicant"):
            if hasattr(user.applicant, "student"):
                token["student_id"] = user.applicant.student.id
            else:
                token["applicant_id"] = user.applicant.id
        if hasattr(user, "organization"):
            token["organization_id"] = user.organization.id
        if hasattr(user, "universitycoordinator"):
            token["university_coordinator_id"] = user.universitycoordinator.id
        if hasattr(user, "universitysupervisor"):
            token["university_supervisor_id"] = user.universitysupervisor.id
        return token