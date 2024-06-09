from rest_framework import serializers
from django.contrib.auth import get_user_model
from .user_serializer import UserCreateSerializer
from .models import *
from posts.models import Application, PostStatus

class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ["id", "first_name", "last_name", "email", "password", "age", "gender", "phone_number", "avatar","resume", "portfolio_link", "date_joined", "is_active"]
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
    post_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "email", "password", "age", "gender", "phone_number", "resume", "portfolio_link", "university", "university_id_number","batch","department", "date_joined", "post_id"]
        extra_kwargs = {
            'password' : {'write_only' : True},
            'date_joined' : {"read_only": True}
        }

    def get_post_id(self, student: Student):
        applicant_pk = student.applicant.id
        accepted_applications = Application.objects.select_related("post").filter(applicant=applicant_pk, status = "accepted")
        posts = [app.post for app in accepted_applications]
        for post in posts:
            status = PostStatus.objects.get(post=post, applicant=applicant_pk)
            if status.allow_supervisor:
                return post.id
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.resolver_match and 'pk' in request.resolver_match.kwargs:
            representation["post_id"] = self.get_post_id(instance)
        return representation

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        student = super().create(validated_data)
        if password:
            student.set_password(password)
            student.save()
        return student
    
class OrganizationSerializer(serializers.ModelSerializer):
    supervisor = UserCreateSerializer()
    organization_email = serializers.EmailField(source="email")
    organization_phone_number = serializers.CharField(source="phone_number")

    class Meta:
        model = Organization
        fields = ["name", "organization_email", "organization_phone_number", "organization_type", "website", "location_city", "location_state", "description", "logo", "linkedin_url", "registration_date", "supervisor"]
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
