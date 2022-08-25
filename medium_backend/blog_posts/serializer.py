from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from user_accounts.serializer import UserSerializer

from blog_posts.models import Comment, Post, Report, Vote


class ReplySerializer(serializers.ModelSerializer):
    """
    Serializes data of Replies of Comments.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Comment
        fields = ['parent', 'id', 'content', 'created', 'owner']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializes the data of a comment.
    """
    owner = UserSerializer(read_only=True)
    reply = SerializerMethodField()

    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Comment
        fields = [
            'parent', 'id', 'post', 'content', 'created', 'owner', 'reply'
        ]

    def get_reply(self, obj):
        """
        Serializer Method to get reply field.
        """
        if obj.is_parent:
            return ReplySerializer(
                obj.children(), many=True,
                context={'request': self.context['request']}
            ).data

        return None

    def update(self, instance, validated_data):
        """" Allow to update only the content of a comment. """
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Overrides to_representation method to add extra fields.
        """
        representation = super().to_representation(instance)
        representation['parent'] = instance.parent.id if instance.parent else None
        representation['post'] = {
            'id': instance.post.id, 'title': instance.post.title
        }
        return representation


class PostSerializer(serializers.ModelSerializer):
    """ Serializes the data of a posts """
    class Meta:
        """ Meta subclass to define fields. """
        model = Post
        fields = ['id', 'title', 'image', 'content', 'posted_by', 'assigned_tags',
                    'total_votes' ,'created_at', 'updated_at']
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
        print(instance.assigned_tags.all())
        representation['assigned_tags'] = [
            {'id': tag.tag.id, 'name': tag.tag.name} for tag in instance.assigned_tags.all()
        ]
        return representation
    

class ReportSerializer(serializers.ModelSerializer):
    """ Serializes the data of a reports associated with a post. """
    class Meta:
        """ Meta subclass to define fields. """
        model = Report
        fields = ['id', 'type', 'post', 'reported_by', 'status', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def to_representation(self, instance):
        ''' Overrides the default representation of a model instance. '''
        representation = super().to_representation(instance)
        representation['type'] = instance.get_type_display()
        representation['post'] = {
            'id': instance.post.id,
            'title': instance.post.title,
        }
        representation['reported_by'] = {
            'id': instance.reported_by.id,
            'username': instance.reported_by.username,
            'email': instance.reported_by.email,
        }
        return representation

    def update(self, instance, validated_data):
        """ Allow to update only the status and type of a report. """
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class VoteSerializer(serializers.ModelSerializer):
    """
    Serializes the data of Votes on Posts.
    """
    class Meta:
        """
        Meta subclass to define fields.
        """
        model = Vote
        fields = ['url', 'id', 'user', 'post', 'u_vote']
        read_only_fields = ('user', 'post')

    def to_representation(self, instance):
        """
        Overrides the default representation of a model instance.
        """
        representation = super().to_representation(instance)
        representation['post'] = {
            'id': instance.post.id,
            'title': instance.post.title,
        }
        representation['user'] = {
            'id': instance.user.id,
            'username': instance.user.username,
        }
        return representation
