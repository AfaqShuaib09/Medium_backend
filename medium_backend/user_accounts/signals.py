''' Signals definition for userApp '''
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from user_accounts.models import Profile


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Display Password reset token on console after creation
    """
    reset_password_token = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                reset_password_token.key)
    print('\n' ,"*"*65)
    print("reset_password_token: {}".format(reset_password_token))
    print("*"*65, '\n')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile associated with a User.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves Profile data associated with a User.
    """
    instance.profile.save()
