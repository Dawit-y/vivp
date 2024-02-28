from rest_framework import routers
# from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("applicants", views.ApplicantViewSet)


urlpatterns = router.urls