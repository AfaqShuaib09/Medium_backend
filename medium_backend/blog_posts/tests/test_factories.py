from datetime import datetime
from factory.django import DjangoModelFactory
from factory import LazyAttribute, PostGenerationMethodCall, SubFactory

from user_accounts.tests.test_factories import UserFactory
from blog_posts.models import Post, Tag, AssignedTag, Vote, Comment, Report

class PostFactory(DjangoModelFactory):
    """
    Factory for Post model to be used for testing purposes.
    """
    class Meta:
        model = Post
        django_get_or_create = ('title', 'posted_by')

    title = 'Test Post'
    content = 'Test Content'
    created_at = LazyAttribute(lambda obj: datetime.now())
    posted_by = SubFactory(UserFactory)
    # posted_by = LazyAttribute(lambda obj: UserFactory())

class TagFactory(DjangoModelFactory):
    """
    Factory for Tag model to be used for testing purposes.
    """
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = 'Test Tag'

class AssignedTagFactory(DjangoModelFactory):
    """
    Factory for AssignedTag model to be used for testing purposes.
    """
    class Meta:
        model = AssignedTag
        django_get_or_create = ('post', 'tag')

    post = SubFactory(PostFactory)
    tag = SubFactory(TagFactory)

class VoteFatory(DjangoModelFactory):
    """
    Factory for Vote model to be used for testing purposes.
    """
    class Meta:
        model = Vote
        django_get_or_create = ('post', 'user')

    u_vote = True
    post = SubFactory(PostFactory)
    user = SubFactory(TagFactory)


class CommentFactory(DjangoModelFactory):
    """
    Factory for Comment model to be used for testing purposes.
    """
    class Meta:
        model = Comment
        django_get_or_create = ('content', 'post', 'owner')

    parent = None
    post = SubFactory(PostFactory)
    owner = SubFactory(UserFactory)
    content = 'Test comment'

class ReportFactory(DjangoModelFactory):
    """
    Factory for Report model to be used for testing purposes.
    """
    class Meta:
        model = Report
        django_get_or_create = ('post', 'reported_by')

    type = 'spam'
    post = SubFactory(PostFactory)
    reported_by = SubFactory(UserFactory)
    status = 'pending'
    