from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register("applicants", views.ApplicantViewSet)
router.register("students", views.StudentViewSet)
router.register("organizations", views.OrganiztionViewSet)
router.register("UvCoordniators", views.UniversityCoordinatorViewSet)
router.register("UvSupervisors", views.UniversitySupervisorViewSet)
router.register("systemCoordinators", views.SystemCoordinatorViewSet, basename="system-coordinator")

applications_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
applications_router.register('applications', views.ApplicantApplicationsViewSet, basename="application-applicant")

certificates_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
certificates_router.register('certificates', views.ApplicantCertificatesViewSet, basename="certificate-applicant")

notifications_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
notifications_router.register('notifications', views.ApplicantNotificationsViewSet, basename="notification-applicant")

evaluatons_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
evaluatons_router.register('evaluations', views.ApplicantEvaluationViewSet, basename="evaluation-applicant")

submitted_tasks_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
submitted_tasks_router.register('submitted_tasks', views.ApplicantSubmittedTasks, basename="submitted-tasks-applicant")

organization_post_router= routers.NestedDefaultRouter(router, 'organizations',lookup='organization')
organization_post_router.register('posts', views.OrganizationPostViewSet, basename="organization_post")

organization_submittedtaks_router=routers.NestedDefaultRouter(router,'organizations',lookup='organization')
organization_submittedtaks_router.register('submitted_tasks', views.OrganizationSubmittedTasksView, basename="organization_submitted_tasks")

evaluate_router = routers.NestedDefaultRouter(organization_submittedtaks_router, 'submitted_tasks', lookup='submitted_tasks')
evaluate_router.register('evaluate', views.EvaluateViewSet, basename='evaluate')

organization_application_router = routers.NestedDefaultRouter(router,'organizations',lookup='organization')
organization_application_router.register('applications', views.OrganizationApplicationViewSet, basename="organization_application")

uvcoordinator_assign = routers.NestedDefaultRouter(router,'UvCoordniators',lookup='UvCoordniators')
uvcoordinator_assign.register('assignments', views.UvCoordinatorassignment, basename="UvCoordniators_assignment")

system_coordinator_posts_router = routers.NestedDefaultRouter(router, 'systemCoordinators', lookup='systemCoordinators')
system_coordinator_posts_router.register("posts", views.SystemCoordinatorPosts, basename="system-coordinator-posts")

system_coordinator_applications_router = routers.NestedDefaultRouter(router, 'systemCoordinators', lookup='systemCoordinators')
system_coordinator_applications_router.register("applications", views.SystemCoordinatorApplications, basename="system-coordinator-applications")


urlpatterns = (
    router.urls +
    applications_router.urls +
    certificates_router.urls +
    notifications_router.urls +
    evaluatons_router.urls +
    submitted_tasks_router.urls +
    organization_post_router.urls +
    organization_submittedtaks_router.urls +
    organization_application_router.urls+
    evaluate_router.urls+
    uvcoordinator_assign.urls+
    system_coordinator_posts_router.urls+
    system_coordinator_applications_router.urls
    
)