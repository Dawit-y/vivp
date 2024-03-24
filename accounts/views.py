from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .serializers import *
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

class ApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Application.objects.filter(applicant__id=applicant_pk)
    
class CertificatesViewSet(ModelViewSet):
    serializer_class = CertificateSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Certificate.objects.filter(applicant__id=applicant_pk)
    
class NotificationsViewSet(ModelViewSet):
    serializer_class = NotificationsSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Notification.objects.filter(notify_to__id=applicant_pk)
    
class EvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    http_method_names = ["get", "head"]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Evaluation.objects.filter(applicant__id=applicant_pk)

