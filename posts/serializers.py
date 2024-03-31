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
        fields = ['title','duration','created','updated','status','sections_count']
 
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
    
    def create(self,validated_data):
        post_pk = self.context.get('post_pk')
        post = get_object_or_404(Post, id=post_pk)
        task = Task.objects.create(
            post = post,
            **validated_data
        )
        
        return task
class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSection
        fields = ['title','content','is_file','is_url','is_text','updated','created']
    def create(self,validated_data):
        task_pk = self.context.get('task_pk')
        task = get_object_or_404(Task, id=task_pk)
        task_section = TaskSection.objects.create(
            task=task,
            **validated_data
        )
        
        return task_section
    


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['skills','cover_letter','availability','other','created','updated']
    def create(self,validated_data):
        post_pk = self.context.get('post_pk')
        post = get_object_or_404(Post, id=post_pk)
        requirement = Requirement.objects.create(
            post = post,
            **validated_data
        )
        return requirement  
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
        fields = ['status','skills','cover_letter','availability','other','updated','created']
    def create(self,validated_data):
        post_pk = self.context.get('post_pk')
        # applicant_pk = self.context.get('applicants_pk')
        # print(applicant_pk)
        post = get_object_or_404(Post, id=post_pk)
        # applicant = get_object_or_404(Applicant, id=applicant_pk)
         
        application = Application.objects.create(
            post=post,
            # applicant=applicant,
            **validated_data
        )
        
        
        return application

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

