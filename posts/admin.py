from django.contrib import admin
from .models import *
from .forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(Post, PostAdmin)
admin.site.register(Task)
admin.site.register(TaskSubmission)
admin.site.register(TaskSection)
admin.site.register(Requirement)
admin.site.register(Evaluation)
admin.site.register(Application)
admin.site.register(Certificate)
admin.site.register(Assignment)
admin.site.register(PaidApplicant)
admin.site.register(PostStatus)
admin.site.register(TaskStatus)