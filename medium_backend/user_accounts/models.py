''' Models related to user accounts '''
from email.policy import default

from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from user_accounts.constant import (CNIC_VALIDATOR, CONTACT_NO_VALIDATOR,
                                    GENDER_CHOICES)
from user_accounts.validators import validate_file_extension


# Create your models here.
class Profile(models.Model):
    ''' User Profile Model '''

    def nameFile(instance, filename):
        ''' uploads the profile picture to the username folder inside media folder'''
        return '/'.join(['images', str(instance.full_name), filename])
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,
                                    help_text='your full name',
                                    blank=True
                                )
    cnic = models.CharField(max_length=15 ,
                                help_text='your CNIC in the following format: xxxxx-xxxxxxx-x',
                                validators=[ CNIC_VALIDATOR ],
                                blank=True
                            )
    contact_number = models.CharField(max_length=13,
                                        help_text='your contact number in the following format: +xxxxxxxxxxx',
                                        validators=[ CONTACT_NO_VALIDATOR ],
                                        blank=True
                                    )
    address = models.TextField(help_text='your address', blank=True)
    country = CountryField(blank_label='(select country)', help_text='your country', blank=True, default='PK')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='', blank=True)
    bio = models.TextField(help_text='your bio', blank=True)
    profile_pic = models.ImageField(upload_to=nameFile, blank=True, validators = [validate_file_extension],
                                        default='images/default/default_user.png')

    def __str__(self):
        ''' Overrides the str method to return the name of the user '''
        return f'{self.user.username} Profile'
