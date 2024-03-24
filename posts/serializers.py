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
        fields = "__all__"