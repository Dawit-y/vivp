from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Student)
admin.site.register(Organization)
admin.site.register(UniversityCoordinator)
admin.site.register(UniversitySupervisor)
admin.site.register(Notification)