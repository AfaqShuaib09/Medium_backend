''' urls definition for user accounts app '''
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from blog_posts.views import PostViewSet, CommentViewSet, PostCommentViewSet, ReportPostViewSet, ReviewReportViewSet, VotePostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'post_comment', PostCommentViewSet , basename='comment')
router.register(r'reports', ReportPostViewSet, basename='report')
router.register(r'review_reports', ReviewReportViewSet, basename='review_report')
router.register(r'votes', VotePostViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]
