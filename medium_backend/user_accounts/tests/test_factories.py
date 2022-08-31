from factory.django import DjangoModelFactory
from factory import LazyAttribute, PostGenerationMethodCall

from django.contrib.auth.models import User

from user_accounts.models import Profile

class UserFactory(DjangoModelFactory):
    """
    Factory for User model to be used for testing purposes.
    """
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'test'
    email = LazyAttribute(lambda obj: '{}@test.com'.format(obj.username))
    password = PostGenerationMethodCall('set_password', 'testqweasd')
    is_active = True


class ProfileFactory(DjangoModelFactory):
    """
    Factory for Profile model to be used for testing purposes.
    """
    class Meta:
        model = Profile
        django_get_or_create = ('user',)
