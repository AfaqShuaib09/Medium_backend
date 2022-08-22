''' validaors definitions for user_accounts app '''
import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ''' validates the file extension for uploaded image file '''
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
