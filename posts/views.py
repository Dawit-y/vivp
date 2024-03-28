from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class PostApplicationsViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Application.objects.filter(post__id=post_pk)

class PostTaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("post_pk")
        return Task.objects.filter(post__id=post_pk)

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
class TaskSectionsViewSet(ModelViewSet):
    serializer_class = TaskSectionSerializer
    def get_queryset(self):
        task_pk = self.kwargs.get("task_pk")
        return TaskSection.objects.filter(task__id=task_pk)
    
class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filterset_fields = ["applicant", "post", "status"]

class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    filterset_fields = ["applicant", "post"]

class EvaluationViewSet(ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    filterset_fields = ["applicant", "task"]