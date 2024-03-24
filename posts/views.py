from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
# Create your views here.
def PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializers_class = PostSerializer