from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import *

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'organization', 'title', 'description', 'image', 'type', 'level', 'category', 'duration', 'updated', 'created', 'is_approved']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
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
        evaluation = Evaluation(**validated_data)
        submitted_pk = self.context['submitted_pk']
        print("hello",submitted_pk)
        task_submission = get_object_or_404(TaskSubmission, id=submitted_pk)
        evaluation.task = task_submission.task
        evaluation.applicant = task_submission.applicant
        evaluation.save()
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
        UvCoordniators_pk = self.context.get('UvCoordniators_pk')
        assignment = Assignment(**validated_data)
        
        uvcoordinator = get_object_or_404(UniversityCoordinator, id=UvCoordniators_pk)
        assignment.coordinator = uvcoordinator
        print('hello',uvcoordinator)
        assignment.save()
        print('there',assignment)
        return assignment


