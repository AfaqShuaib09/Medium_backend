import os

from django.test import TestCase
from user_accounts.validators import validate_file_extension


class TestValidator(TestCase):
    """ Test class to check validator behaviour """
    def test_validator_with_valid_file_extension(self):
        """ Test to validate the img file extension """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../media/images/Default/default_user.png')
        image = open(filename, 'rb')
        valid_image_ext = validate_file_extension(image)
        assert valid_image_ext == True