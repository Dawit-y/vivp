from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.simple_serializer import *

from .models import *
from accounts.serializers import ApplicantSerializer, OrganizationSerializer

class PostSerializer(serializers.ModelSerializer):
    system_coordinator = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True, is_superuser=False), required=False, allow_null=True)
    tasks_count = serializers.SerializerMethodField(method_name="get_tasks_count")
    organization = SimpleOrganizationSerializer()
    class Meta:
        model = Post
        fields = "__all__"

    def get_tasks_count(self, post: Post):
        return post.get_tasks().count()
       
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tasks_count'] = self.get_tasks_count(instance)
        return representation
    
    def validate(self, attrs):
        system_coordinator = attrs.get('system_coordinator')
        organization = attrs.get('organization')

        if organization and system_coordinator:
            raise serializers.ValidationError('Only one of organization or system coordinator should be set.')
        if not organization and not system_coordinator:
            raise serializers.ValidationError('Either organization or system coordinator must be set.')
        return attrs

class PostCreateSerializer(serializers.ModelSerializer):
    system_coordinator = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=True, is_superuser=False), required=False, allow_null=True)
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_tasks_count(self, post: Post):
        return post.get_tasks().count()

    def validate(self, attrs):
        system_coordinator = attrs.get('system_coordinator')
        organization = attrs.get('organization')

        if organization and system_coordinator:
            raise serializers.ValidationError('Only one of organization or system coordinator should be set.')
        if not organization and not system_coordinator:
            raise serializers.ValidationError('Either organization or system coordinator must be set.')
        return attrs

    def create(self, validated_data):
        system_coordinator = validated_data.pop('system_coordinator', None)
        organization = validated_data.pop('organization', None)

        post = Post.objects.create(**validated_data)

        if system_coordinator:
            post.system_coordinator = system_coordinator
            post.save()
        elif organization:
            post.organization = organization
            post.save()

        return post
class TaskSerializer(serializers.ModelSerializer):
    sections_count = serializers.SerializerMethodField(method_name="get_task_section_count")
    post_id = serializers.SerializerMethodField(method_name="get_post_id")

    class Meta:
        model = Task
        fields = ['title','duration','sections_count','post_id','created','updated',]
 
    def get_task_section_count(self, task: Task):
        return task.get_task_sections().count()
    
    def get_post_id(self, task: Task):
        return task.post.id
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["sections_count"] = self.get_task_section_count(instance)
        representation["post_id"] = self.get_post_id(instance)
        return representation
    
    def create(self,validated_data):
        post_pk = self.context.get('post_pk')
        post = get_object_or_404(Post, id=post_pk)
        task = Task.objects.create(
            post = post,
            **validated_data
        )
        
        return task
    
class TaskOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class TaskSectionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        task_pk = self.context.get('task_pk')
        task = get_object_or_404(Task, id=task_pk)
        task_sections = [TaskSection(task=task, **item) for item in validated_data]
        return TaskSection.objects.bulk_create(task_sections)

class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSection
        fields = ['title','content', 'video','is_file','is_url','is_text','updated','created']
        list_serializer_class = TaskSectionListSerializer
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
    
class SimplePostSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Post
        fields = ['id', 'organization', 'title', 'type', 'level', 'category', 'duration']

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = SimpleApplicantSerializer()
    post = SimplerPostSerializer()
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["applicant", "post"]

class AddApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(queryset=Applicant.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Application
        fields = "__all__"
    
class PostApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ["applicant",'status','skills','cover_letter','availability','other','updated','created']

    def create(self,validated_data):
        post_pk = self.context.get('post_pk')
        post = get_object_or_404(Post, id=post_pk)   
        application = Application.objects.create(
            post=post,
            **validated_data
        )
        return application

class CertificateSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    post = SimplePostSerializer()
    class Meta:
        model = Certificate
        fields = ["applicant", "post", "pdf_file", "updated", "created"]

class EvaluationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluation
        fields = ['comment','proficiency_level','skills_learned','updated','created']

    def validate(self, data):
        submitted_pk = self.context.get("submitted_pk")
        existing_evaluation = Evaluation.objects.filter(submitted_task_id=submitted_pk).exists()
        if existing_evaluation:
            raise serializers.ValidationError("An evaluation already exists for this submitted task.", code="unique")
        return data

    def create(self,validated_data):
        submitted_pk = self.context.get('submitted_pk')
        task_submission = get_object_or_404(TaskSubmission, id=submitted_pk)
        evaluation = Evaluation.objects.create(
            submitted_task=task_submission,
            applicant=task_submission.applicant,
            **validated_data
        )
        
        return evaluation
    
class TaskSubmissionSerializer(serializers.ModelSerializer):
    task = TaskSerializer()
    applicant = SimpleApplicantSerializer()
    status = serializers.SerializerMethodField(method_name="get_status")
    
    class Meta:
        model = TaskSubmission
        fields =["id", "status", "submited_url", "submited_file", "submitted_text", "task", "applicant", "updated", "created"]

    def get_status(self, submitted: TaskSubmission):
            task = submitted.task
            applicant = submitted.applicant
            try:
                task_status = TaskStatus.objects.get(task=task, applicant=applicant)
                return task_status.status
            except TaskStatus.DoesNotExist:
                print("Task status does not exist for the given task and applicant.")
                return None  # or handle the absence of a status as needed
            except TaskStatus.MultipleObjectsReturned:
                print("Multiple task statuses found for the given task and applicant.")
                return None  # or handle the presence of multiple statuses as needed
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["status"] = self.get_status(instance)
        return representation
        
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['student', 'supervisor', 'updated', 'created']

    def create(self, validated_data):
        uv_coordinators_pk = self.context.get('UvCoordniators_pk')
        uv_coordinator = get_object_or_404(UniversityCoordinator, id=uv_coordinators_pk)

        if isinstance(validated_data, list):
            assignments = [Assignment(coordinator=uv_coordinator, student=data['student'], supervisor=data['supervisor'], updated=data['updated'], created=data['created']) for data in validated_data]
            return Assignment.objects.bulk_create(assignments)
        else:
            assignment = Assignment(coordinator=uv_coordinator, **validated_data)
            assignment.save()
            return assignment
class SupervisorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorComment
        fields = '__all__'

class SupervisorEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorEvaluation
        fields = '__all__'

    def create(self, validated_data):
        if isinstance(validated_data, list):
            evaluations = [SupervisorEvaluation(**data) for data in validated_data]
            return SupervisorEvaluation.objects.bulk_create(evaluations)
        else:
            evaluation = SupervisorEvaluation(**validated_data)
            evaluation.save()
            return evaluation

class PostStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostStatus
        fields = "__all__"

class TaskStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskStatus
        fields = "__all__"