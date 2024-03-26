from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.generics import GenericAPIView

from .models import *
from .serializers import *


class PostListRetrieveView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.kwargs.get('pk'):
            return PostDetailSerializer
        else:
            return PostListSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
    
class PostApplicationsListRetrieveView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get("pk")
        return Application.objects.filter(post__pk = post_pk)
    
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
    
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