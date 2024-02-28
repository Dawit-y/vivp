from rest_framework import serializers

from .models import *

class ApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Applicant
        fields = ["id", "first_name", "last_name", "email", "password", "phone_number", "resume", "date_joined"]