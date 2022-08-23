''' urls definition for user accounts app '''
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog_posts.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]
