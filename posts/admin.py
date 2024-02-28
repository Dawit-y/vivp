from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Task)
admin.site.register(TaskSubmission)
admin.site.register(Requirement)
admin.site.register(Evaluation)
admin.site.register(Application)
admin.site.register(Certificate)
admin.site.register(Assignment)