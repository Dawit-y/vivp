from django.urls import path

from rest_framework import routers
from . import views

router = routers.DefaultRouter()

# router.register("posts",views.PostViewSet,basename='posts')


urlpatterns = [
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
] + router.urls