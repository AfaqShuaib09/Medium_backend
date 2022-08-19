""" Admin panel for the user accounts module """
from django.contrib import admin

from user_accounts.models import Profile

# Register your models here.

admin.site.register(Profile)
