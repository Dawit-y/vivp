from rest_framework import serializers

from .models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = "__all__"

    def get_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            if hasattr(user, 'applicant'):
                applicant = user.applicant
                try:
                    task_submission = TaskSubmission.objects.get(
                        applicant=applicant,
                        task=obj
                    )
                    return task_submission.status
                except TaskSubmission.DoesNotExist:
                    return None
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = self.get_status(instance)
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
        fields = "__all__"