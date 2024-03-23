from rest_framework import routers
# from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("applicants", views.ApplicantViewSet)
router.register("students", views.StudentViewSet)
router.register("organizations", views.OrganiztionViewSet)


urlpatterns = router.urls