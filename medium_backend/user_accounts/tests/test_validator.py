import os

from django.core.exceptions import ValidationError
from django.test import TestCase
from user_accounts.validators import validate_file_extension


class TestValidators(TestCase):
    """ Test class to check validator behaviour """
    def test_validator_with_valid_file_extension(self):
        """ Test to validate the img file extension """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../media/images/Default/default_user.png')
        image = open(filename, 'rb')
        valid_image_ext = validate_file_extension(image)
        assert valid_image_ext == True

    def test_validator_with_invalid_file_extension(self):
        """ Test to validate the img file extension """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../media/images/Default/default_user.txt')
        image = open(filename, 'rb')
        with self.assertRaises(ValidationError):
            validate_file_extension(image)
