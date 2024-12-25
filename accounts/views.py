from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework import status

from .user_serializer import UserCreateSerializer, UserSerializer
from .serializers import *
from .permissions import *
from posts.serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .user_serializer import MyTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            refresh_token = response.data.pop("refresh", None)
            if refresh_token:
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=True,  # Use True in production with HTTPS
                    samesite="None"
                )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        mutable_data = request.data.copy()
        mutable_data["refresh"] = refresh_token
        request._full_data = mutable_data

        # Call the parent post method to get the tokens
        response = super().post(request, *args, **kwargs)

        # Check if the response is successful and modify it
        if response.status_code == 200:
            refresh = response.data.pop("refresh", None)  # Remove the refresh token from the JSON response
            if refresh:
                # Set the refresh token as an HTTP-only cookie
                response.set_cookie(
                    key="refresh_token",
                    value=refresh,
                    httponly=True,
                    secure=True,  # Set to False in development if HTTPS is not used
                    samesite="None",
                    max_age=7 * 24 * 60 * 60  # Set cookie expiry to 7 days
                )
        return response

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        return response

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

class SystemCoordinatorViewSet(ModelViewSet):

    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_superuser=False)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer
    
    def perform_create(self, serializer):
        serializer.validated_data['is_staff'] = True 
        instance = serializer.save() 
        return instance
    
class ApplicantApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Application.objects.filter(applicant__id=applicant_pk)
    
class ApplicantAcceptedPostsViewSet(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        accepted_applications = Application.objects.select_related("post").filter(applicant=applicant_pk, status = "accepted")
        return [app.post for app in accepted_applications]
    
class ApplicantCertificatesViewSet(ModelViewSet):
    serializer_class = CertificateSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Certificate.objects.filter(applicant__id=applicant_pk)
    
class ApplicantNotificationsViewSet(ModelViewSet):
    serializer_class = NotificationsSerializer
    http_method_names = ['get', 'head', 'options', 'put', 'patch']
    permission_classes = [IsApplicant | IsSuperUser]

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Notification.objects.filter(notify_to__id=applicant_pk)
    
class ApplicantSubmittedTasks(ModelViewSet):
    serializer_class = TaskSubmissionSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        post_id = self.request.query_params.get('post_id')
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            tasks = post.get_tasks()
            return TaskSubmission.objects.filter(applicant__id=applicant_pk, task__in=tasks)
        return TaskSubmission.objects.filter(applicant__id=applicant_pk)
     
class ApplicantEvaluationViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        applicant_pk = self.kwargs.get("applicant_pk")
        return Evaluation.objects.filter(applicant__id=applicant_pk)

class OrganizationPostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    filterset_fields = ["type"]

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        return Post.objects.filter(organization_id=organization_pk)
    
class OrganizationSubmittedTasksView(ModelViewSet):
    serializer_class = TaskSubmissionSerializer
    http_method_names = ['get', 'head', 'options']
    
    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        posts = Post.objects.filter(organization_id=organization_pk)
        submitted_tasks = TaskSubmission.objects.filter(task__post__in=posts)
        return submitted_tasks
class OrganizationApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'options', 'put', 'patch']

    def get_queryset(self):
        organization_pk = self.kwargs.get("organization_pk")
        posts = Post.objects.filter(organization_id=organization_pk)
        applications = Application.objects.filter(post__in = posts)
        return applications
    
class UvCoordinatorAssignmentViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        UvCoordniators_pk = self.kwargs.get("UvCoordniators_pk")
        return Assignment.objects.filter(coordinator_id=UvCoordniators_pk)

    def get_serializer_context(self, *args, **kwargs):
        UvCoordniators_pk = self.kwargs.get("UvCoordniators_pk")
        return {'UvCoordniators_pk': UvCoordniators_pk}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
class UvCoordinatorStudents(ModelViewSet):
    serializer_class = StudentSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        UvCoordniators_pk = self.kwargs.get("UvCoordniators_pk")
        uv_coordinator = get_object_or_404(UniversityCoordinator, id=UvCoordniators_pk)
        return uv_coordinator.get_students()
    
class UvCoordinatorAcceptedStudents(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddAcceptedStudentsSerializer
        return AcceptedStudentsSerializer

    def get_queryset(self):
        UvCoordniators_pk = self.kwargs.get("UvCoordniators_pk")
        uv_coordinator = get_object_or_404(UniversityCoordinator, id=UvCoordniators_pk)
        return AcceptedStudents.objects.filter(coordinator=uv_coordinator)
         

class UvSupervisorStudents(ModelViewSet):
    serializer_class = StudentSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        UvSupervisor_pk = self.kwargs.get("UvSupervisors_pk")
        uv_supervisor = get_object_or_404(UniversitySupervisor, id=UvSupervisor_pk)
        return uv_supervisor.get_students()


 
class SupervisorEvaluationViewSet(ModelViewSet):
    serializer_class = SupervisorEvaluationSerializer

    def get_queryset(self):
        print(self.kwargs)
        UvSupervisor_pk = self.kwargs.get("UvSupervisors_pk")
        uv_supervisor = get_object_or_404(UniversitySupervisor, id=UvSupervisor_pk)
        return SupervisorEvaluation.objects.filter(supervisor=uv_supervisor)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save() 
        
class EvaluateViewSet(ModelViewSet):
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        submitted_pk = self.kwargs.get("submitted_tasks_pk")
        task_submission = get_object_or_404(TaskSubmission, id=submitted_pk)
        return Evaluation.objects.filter(submitted_task=task_submission)
    
    def get_serializer_context(self, *args, **kwargs):
        submitted_pk=self.kwargs.get("submitted_tasks_pk")
        return {'submitted_pk':submitted_pk }       

class SystemCoordinatorPosts(ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        system_coordinator_pk = self.kwargs.get("systemCoordinators_pk")
        return Post.objects.filter(system_coordinator_id=system_coordinator_pk)
    
    def perform_create(self, serializer):
        system_coordinator_pk = self.kwargs.get("systemCoordinators_pk")
        serializer.validated_data['system_coordinator'] = system_coordinator_pk
        instance = serializer.save()
        return instance
class SystemCoordinatorSubmittedTasksView(ModelViewSet):
    serializer_class = TaskSubmissionSerializer
    http_method_names = ['get', 'head', 'options']
    
    def get_queryset(self):
        system_coordinator_pk = self.kwargs.get("systemCoordinators_pk")
        posts = Post.objects.filter(system_coordinator_id=system_coordinator_pk)
        submitted_tasks = TaskSubmission.objects.filter(task__post__in=posts)
        return submitted_tasks   
class SystemCoordinatorApplications(ModelViewSet):
    serializer_class = ApplicationSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        system_coordinator_pk = self.kwargs.get("systemCoordinators_pk")
        posts = Post.objects.filter(system_coordinator_id=system_coordinator_pk)
        applications = Application.objects.filter(post__in = posts)
        return applications
    