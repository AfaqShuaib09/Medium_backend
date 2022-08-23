from rest_framework import serializers

from blog_posts.models import Post, Tag, AssignedTag

class PostSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'content', 'posted_by', 'created_at', 'updated_at']
        read_only_fields = ('posted_by',)
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def to_representation(self, instance):
        ''' Overrides the default representation of a model instance. '''
        representation = super().to_representation(instance)
        representation['posted_by'] = {
            'id': instance.posted_by.id,
            'username': instance.posted_by.username,
            'email': instance.posted_by.email,
        }
        return representation
