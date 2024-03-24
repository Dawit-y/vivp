from rest_framework import serializers

from .models import *
class postserializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'organization', 'title', 'description', 'image', 'type', 'level', 'category', 'skills_gained', 'duration', 'updated', 'created', 'is_approved']