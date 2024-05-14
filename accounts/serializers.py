from rest_framework import serializers
from django.contrib.auth import get_user_model
from .user_serializer import UserCreateSerializer
from .models import *

class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ["id", "first_name", "last_name", "email", "password", "age", "gender", "phone_number", "avatar","resume", "portfolio_link", "date_joined"]
        extra_kwargs = {
            'password' : {'write_only' : True},
            'date_joined' : {"read_only": True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        applicant = super().create(validated_data)
        if password:
            applicant.set_password(password)
            applicant.save()
        return applicant

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "email", "password", "age", "gender", "phone_number", "resume", "portfolio_link", "university", "university_id_number","batch","department", "date_joined"]
        extra_kwargs = {
            'password' : {'write_only' : True},
            'date_joined' : {"read_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        student = super().create(validated_data)
        if password:
            student.set_password(password)
            student.save()
        return student
    
class OrganizationSerializer(serializers.ModelSerializer):
    supervisor = UserCreateSerializer()
    
    class Meta:
        model = Organization
        fields = ["name", "email", "phone_number", "organization_type", "website", "location_city", "location_state", "description", "logo", "linkedin_url", "registration_date", "supervisor"]
        extra_kwargs = {
            'registration_date' : {"read_only": True}
        }

    def create(self, validated_data):
        supervisor = dict(validated_data.pop("supervisor"))
        instance = get_user_model().objects.create(**supervisor)
        instance.set_password(supervisor["password"])
        instance.is_staff = False
        instance.save()
        return Organization.objects.create(supervisor=instance, **validated_data)

class UvCoordinatorSerializer(serializers.ModelSerializer):

    class Meta:
        model=UniversityCoordinator
        fields = ["id", "first_name", "last_name", "email", "password", "phone_number","university", "legal_document", "date_joined"]
        extra_kwargs = {
                'password' : {'write_only' : True},
                'date_joined' : {"read_only": True}
            }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        uvcoordinator = super().create(validated_data)
        if password:
            uvcoordinator.set_password(password)
            uvcoordinator.save()
        return uvcoordinator

class UvSupervisorSerializer(serializers.ModelSerializer):

    class Meta:
        model=UniversitySupervisor
        fields = ["id", "first_name", "last_name", "email", "password", "phone_number", "department", "coordinator", "specialization","date_joined"]
        extra_kwargs = {
            'password' : {'write_only' : True},
            'date_joined' : {"read_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        uvsupervisor = super().create(validated_data)
        if password:
            uvsupervisor.set_password(password)
            uvsupervisor.save()
        return uvsupervisor

class NotificationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"
