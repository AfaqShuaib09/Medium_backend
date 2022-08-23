from cgitb import lookup
from turtle import title
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from blog_posts.models import Post
from blog_posts.serializer import PostSerializer
from blog_posts.constant import POST_REQ_FIELDS

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    ''' API endpoint that allows posts to be viewed, created, updated or deleted. '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'
    
    def create(self, request, *args, **kwargs):
        ''' Create a new post associated with the user. '''
        # if some field is missing, return error
        for field in POST_REQ_FIELDS:
            if field not in request.data:
                return Response({field: 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        post = Post.objects.create(
            posted_by = request.user,
            title = request.data.get('title', ''),
            image = request.data.get('image'),
            content = request.data.get('content', ''),
        )
        post.save()
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
