from django.urls import path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register("applications",views.ApplicationViewSet)
router.register("certificates",views.CertificateViewSet)
router.register("evaluations",views.EvaluationViewSet)



urlpatterns = [
    path('posts/', views.PostListRetrieveView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostListRetrieveView.as_view(), name='post-detail'),
    path('posts/<int:pk>/applications/', views.PostApplicationsListRetrieveView.as_view(), name="post-applications-list"),
    path('posts/<int:pk>/applications/<int:id>/', views.PostApplicationsListRetrieveView.as_view(), name="post-applications-detail"),
] + router.urls