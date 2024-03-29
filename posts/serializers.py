from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import *

class PostSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField(method_name="get_tasks_count")
    status = serializers.SerializerMethodField(method_name="get_status")
    class Meta:
        model = Post
        fields = "__all__"

    def get_tasks_count(self, post: Post):
        return post.get_tasks().count()
    
    def get_status(self, post: Post):
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            return "Unauthenticated User"
        
        user = request.user
        
        if not hasattr(user, 'applicant'):
            return "Unauthorized Access"
        
        applicant: Applicant = user.applicant
        
        try:
            application = Application.objects.filter(applicant=applicant, post=post).latest('created')
            if application.status == "accepted":
                submitted_tasks = applicant.get_submitted_tasks()
                if all(task.status == "Completed" for task in submitted_tasks):
                    return "Completed"
                else:
                    return "Inprogress"
            else:
                return f"{application.status} application"
        except Application.DoesNotExist:
            return "Not Applied"
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tasks_count'] = self.get_tasks_count(instance)
        representation["status"] = self.get_status(instance)
        return representation

class TaskSerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField(method_name="get_task_section_count")
    status = serializers.SerializerMethodField(method_name="get_status")

    class Meta:
        model = Task
        fields = "__all__"
 
    def get_status(self, obj: Task):
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            return "Unauthenticated User"
        
        user = request.user
        
        if not hasattr(user, 'applicant'):
            return "Unauthorized Access"
        
        applicant: Applicant = user.applicant
        
        try:
            task_submission = TaskSubmission.objects.get(
                applicant=applicant,
                task=obj
            )
            return task_submission.status
        except TaskSubmission.DoesNotExist:
            return "Inprogress"
       
    def get_task_section_count(self, task: Task):
        return task.get_task_sections().count()
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = self.get_status(instance)
        representation["sections_count"] = self.get_task_section_count(instance)
        return representation

class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSection
        fields = "__all__"

class TaskSubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields = "__all__"
class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = "__all__"

class PostDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    requirements = RequirementSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'organization', 'title', 'description', 'image', 'type', 'level', 'category',"skills_gained", 'tasks', 'requirements', 'duration', 'updated', 'created', 'is_approved']
    
    def to_representation(self, instance: Post):
        representation = super().to_representation(instance)
        representation['tasks'] = TaskSerializer(instance.get_tasks(), many=True).data
        representation['requirements'] = RequirementSerializer(instance.get_requirements(), many=True).data
        return representation
    
class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"

class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = "__all__"

class EvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation
        fields = ['comment','grade','updated','created']

    def create(self,validated_data):
        submitted_pk = self.context.get('submitted_pk')
        task_submission = get_object_or_404(TaskSubmission, id=submitted_pk)
        evaluation = Evaluation.objects.create(
            task=task_submission.task,
            applicant=task_submission.applicant,
            **validated_data
        )
        
        return evaluation
    
class TaskSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSubmission
        fields ='__all__'
        
class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['student','supervisor','updated','created']

    def create(self,validated_data):
        uv_coordinators_pk = self.context.get('UvCoordniators_pk')
        uv_coordinator = get_object_or_404(UniversityCoordinator, id=uv_coordinators_pk)
        assignment = Assignment.objects.create(
            coordinator=uv_coordinator,
            **validated_data
        )
        return assignment

