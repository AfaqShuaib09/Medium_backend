from cgitb import lookup
from turtle import title
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from blog_posts.models import Post, Tag, AssignedTag
from blog_posts.serializer import PostSerializer
from blog_posts.constant import POST_REQ_FIELDS
from blog_posts.permissions import PostOwnerOrReadOnly


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

        request.data['tags'] = request.data['tags'].split(',')
        for tag in request.data['tags']:
            if not Tag.objects.filter(name=tag).exists():
                Tag.objects.create(name=tag)
                # assign tag to post
        
        post = Post.objects.create(
            posted_by = request.user,
            title = request.data.get('title', ''),
            image = request.data.get('image'),
            content = request.data.get('content', ''),
        )
        post.save()

        for tag in request.data['tags']:
            tag = Tag.objects.get(name=tag)
            AssignedTag.objects.create(post=post, tag=tag)

        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
