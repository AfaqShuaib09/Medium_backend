''' Signals definition for userApp '''
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Display Password reset token on console after creation
    """
    reset_password_token = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                reset_password_token.key)
    print("*"*65)
    print("reset_password_token: {}".format(reset_password_token))
    print("*"*65, '\n')
