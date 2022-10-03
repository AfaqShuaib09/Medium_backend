''' urls definition for user accounts app '''
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog_posts.views import (CommentViewSet, PostCommentViewSet, PostViewSet,
                              ReportPostViewSet, ReviewReportViewSet,
                              VotePostViewSet, PopularPostsViewSet)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'post_comment', PostCommentViewSet , basename='comment')
router.register(r'reports', ReportPostViewSet, basename='report')
router.register(r'review_reports', ReviewReportViewSet, basename='review_report')
router.register(r'votes', VotePostViewSet, basename='vote')
router.register(r'popular-posts', PopularPostsViewSet, basename='popular-posts')

urlpatterns = [
    path('', include(router.urls)),
]
