from django.shortcuts import get_object_or_404
from rest_framework import serializers

from posts.models import Post, Task

from .models import *

class SimpleApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ['id','first_name', "last_name", "email","phone_number", "gender", "avatar"]

class SimplerPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', "type", "level", "description"]

class SimpleTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "title", "duration"]