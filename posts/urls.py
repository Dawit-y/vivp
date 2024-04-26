from django.urls import path

from rest_framework_nested import routers
from . import views
from .web_hook import Webhook

router = routers.DefaultRouter()

router.register("posts", views.PostViewSet, basename="posts")
router.register("tasks", views.TaskViewSet)
router.register("applications",views.ApplicationViewSet)
router.register("certificates",views.CertificateViewSet)
router.register("evaluations",views.EvaluationViewSet)

applications_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
applications_router.register('applications', views.PostApplicationsViewSet, basename="post-applicaton")

requirements_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
requirements_router.register('requirements', views.PostRequirementsViewSet, basename="post-requirements")

task_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
task_router.register('tasks', views.PostTaskViewSet, basename="post-task")

section_router = routers.NestedDefaultRouter(router, 'tasks', lookup='task')
section_router.register('sections', views.TaskSectionsViewSet, basename="task-section")

urlpatterns = [
    path('payment/<int:post_id>/', views.ProcessPayment.as_view(), name='payment'),
    path("webhook/", Webhook.as_view(), name="webhook")
    
    ] + router.urls + applications_router.urls + task_router.urls + section_router.urls + requirements_router.urls