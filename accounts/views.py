from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


class ApplicantViewSet(ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer