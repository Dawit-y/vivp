from django.urls import path

from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register("posts", views.PostViewSet)
router.register("tasks", views.TaskViewSet)
router.register("applications",views.ApplicationViewSet)
router.register("certificates",views.CertificateViewSet)
router.register("evaluations",views.EvaluationViewSet)

applications_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
applications_router.register('applications', views.PostApplicationsViewSet, basename="post-applicaton")

task_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
task_router.register('tasks', views.PostTaskViewSet, basename="post-task")

section_router = routers.NestedDefaultRouter(router, 'tasks', lookup='task')
section_router.register('sections', views.TaskSectionsViewSet, basename="task-section")

urlpatterns =  router.urls + applications_router.urls + task_router.urls + section_router.urls