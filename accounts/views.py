from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .permissions import *
from posts.serializers import *


class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class OrganiztionViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class UniversityCoordinatorViewSet(ModelViewSet):
    queryset = UniversityCoordinator.objects.all()
    serializer_class = UvCoordinatorSerializer

class UniversitySupervisorViewSet(ModelViewSet):
    queryset = UniversitySupervisor.objects.all()
    serializer_class = UvSupervisorSerializer

class ApplicantApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Application.objects.filter(applicant__id=applicant_pk)
    
class ApplicantCertificatesViewSet(ModelViewSet):
    serializer_class = CertificateSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Certificate.objects.filter(applicant__id=applicant_pk)
    
class ApplicantNotificationsViewSet(ModelViewSet):
    serializer_class = NotificationsSerializer
    http_method_names = ["get", "head"]
    permission_classes = [IsApplicant]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Notification.objects.filter(notify_to__id=applicant_pk)
    
class ApplicantEvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Evaluation.objects.filter(applicant__id=applicant_pk)

class OrganizationPostViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        return Post.objects.filter(organization_id=organization_pk)
class OrganizationSubmittedTasksView(ModelViewSet):
    serializer_class = TaskSubmissionSerializer
    
    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        posts = Post.objects.filter(organization_id=organization_pk)
        submitted_tasks = TaskSubmission.objects.filter(task__post__in=posts, task__status='submitted')
        return submitted_tasks
class OrganizationApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        posts = Post.objects.filter(organization_id=organization_pk)

        applications = Application.objects.filter(post__in = posts)
        return applications
class UvCoordinatorassignment(ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        UvCoordniators_pk = self.kwargs.get("UvCoordniators_pk")
        print('hello',self.kwargs)
        return Assignment.objects.filter(coordinator_id=UvCoordniators_pk)
    def get_serializer_context(self, *args, **kwargs):
        UvCoordniators_pk=self.kwargs.get("UvCoordniators_pk")
        return {'UvCoordniators_pk':UvCoordniators_pk }       

        
class EvaluateViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        submitted_pk = self.kwargs.get("submitted_tasks_pk")
        task_submission = get_object_or_404(TaskSubmission, id=submitted_pk)
        return Evaluation.objects.filter(task = task_submission.task)
    
    def get_serializer_context(self, *args, **kwargs):
        submitted_pk=self.kwargs.get("submitted_tasks_pk")
        return {'submitted_pk':submitted_pk }       
