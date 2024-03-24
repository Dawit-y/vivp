from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register("applicants", views.ApplicantViewSet)
router.register("students", views.StudentViewSet)
router.register("organizations", views.OrganiztionViewSet)
router.register("UvCoordniators", views.UniversityCoordinatorViewSet)
router.register("UvSupervisors", views.UniversitySupervisorViewSet)

applications_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
applications_router.register('applications', views.ApplicationsViewSet, basename="application-applicant")

certificates_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
certificates_router.register('certificates', views.CertificatesViewSet, basename="certificate-applicant")

notifications_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
notifications_router.register('notifications', views.NotificationsViewSet, basename="notification-applicant")

evaluatons_router = routers.NestedDefaultRouter(router, 'applicants', lookup='applicant')
evaluatons_router.register('evaluations', views.EvaluationViewSet, basename="evaluation-applicant")



urlpatterns = router.urls + applications_router.urls + certificates_router.urls + notifications_router.urls + evaluatons_router.urls