from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status, mixins, generics
from rest_framework.response import Response

from blog_posts.models import Post, Tag, AssignedTag, Comment, Report
from blog_posts.serializer import PostSerializer, CommentSerializer, ReportSerializer
from blog_posts.constant import POST_REQ_FIELDS
from blog_posts.permissions import PostOwnerOrReadOnly, CommentOwnerOrReadOnly


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    ''' API endpoint that allows posts to be viewed, created, updated or deleted. '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, PostOwnerOrReadOnly]
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        ''' Create a new post associated with the user. '''
        # if some field is missing, return error
        for field in POST_REQ_FIELDS:
            if field not in request.data:
                return Response({field: 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('tags'):
            request.data['tags'] = request.data['tags'].split(',')
            for tag in request.data['tags']:
                if not Tag.objects.filter(name=tag).exists():
                    Tag.objects.create(name=tag)

        post = Post.objects.create(
            posted_by = request.user,
            title = request.data.get('title', ''),
            image = request.data.get('image'),
            content = request.data.get('content', ''),
        )
        post.save()
        if request.data.get('tags'):
            for tag in request.data['tags']:
                AssignedTag.objects.create(post=post, tag=Tag.objects.get(name=tag))

        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """ Allow to update only the content of a comment. """
        if request.data.get('tags'):
            removed_tags = []
            tags = request.data['tags'].split(',')
            for tag in tags:
                if not Tag.objects.filter(name=tag).exists():
                    Tag.objects.create(name=tag)
            print(self.get_object().assigned_tags.all())
            for tag in self.get_object().assigned_tags.all():
                print(tag.tag.name)
                if tag.tag.name not in tags:
                    removed_tags.append(tag.tag.name)
            # remove all tags that are in removed_tags from assigned_tags
            for tag in removed_tags:
                self.get_object().assigned_tags.get(tag=Tag.objects.get(name=tag), post=self.get_object()).delete()
            # add all tags that are not in assigned_tags from tags
            for tag in tags:
                if not self.get_object().assigned_tags.filter(tag=Tag.objects.get(name=tag),
                                                                post=self.get_object()).exists():
                    AssignedTag.objects.create(post=self.get_object(), tag=Tag.objects.get(name=tag))
        if request.data.get('tags') == '':
            for tag in self.get_object().assigned_tags.all():
                tag.delete()
        return super().update(request, *args, **kwargs)

class CommentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides list and detail, create, update actions for Comment Model.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def perform_create(self, serializer):
        """
        Saves the comment of the currently logged user.
        """
        serializer.save(owner=self.request.user)


class PostCommentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    This viewset list all the comments of the post
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the comments
        for the post of the current user.
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post__id=int(post_id), parent = None)
        return queryset


class ReportPostViewSet(viewsets.ModelViewSet):
    """
    Viewset providing all create, list, update and detail actions for Report Model.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'IntegrityError: Already reported by the user.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Saves the report of the currently logged user.
        """
        serializer.save(reported_by=self.request.user)


class ReviewReportViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """ Allow admin to review the report """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """ update the post report status """
        instance = self.get_object()
        instance.status = request.data.get('status', instance.status)
        instance.save()
        return Response(instance.status, status=status.HTTP_200_OK)
