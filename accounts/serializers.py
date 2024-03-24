from rest_framework import serializers

from .models import *

class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ["id", "first_name", "last_name", "email", "age", "gender", "phone_number", "resume", "portfolio_link", "date_joined"]

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "email", "age", "gender", "phone_number", "resume", "portfolio_link", "university", "university_id_number","batch","department", "date_joined"]

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
class UvCoordinatorSerializer(serializers.ModelSerializer):

    class Meta:
        model=UniversityCoordinator
        fields = ['university','legal_documnet']
class UvSupervisorSerializer(serializers.ModelSerializer):

    class Meta:
        model=UniversitySupervisor
        fields = '__all__'
    