from django.test import TestCase
from user_accounts.tests.constants import (INVALID_CNIC, INVALID_CONTACT_NO,
                                           INVALID_EMAIL, INVALID_GENDER,
                                           INVALID_PASSWORD, INVALID_USERNAME,
                                           VALID_CNIC, VALID_CONTACT_NO,
                                           VALID_EMAIL, VALID_GENDER,
                                           VALID_PASSWORD, VALID_USERNAME)
from user_accounts.utils import (validate_cnic, validate_contact_number,
                                 validate_email, validate_gender,
                                 validate_password, validate_username)


class UtilsTest(TestCase):
    def test_validate_cnic(self):
        """
        Test to validate cnic
        """
        assert validate_cnic(VALID_CNIC) == True
    
    def test_cnic_with_invalid_format(self):
        """
        Test to validate cnic with invalid format
        """
        assert validate_cnic(INVALID_CNIC) == False
    
    def test_validate_contact_number(self):
        """
        Test to validate contact number
        """
        assert validate_contact_number(VALID_CONTACT_NO) == True
    
    def test_contact_number_with_invalid_format(self):
        """
        Test to validate contact number with invalid format
        """
        assert validate_contact_number(INVALID_CONTACT_NO) == False
    
    def test_validate_email(self):
        """
        Test to validate email
        """
        assert validate_email(VALID_EMAIL) == True
    
    def test_email_with_invalid_format(self):
        """
        Test to validate email with invalid format
        """
        assert validate_email(INVALID_EMAIL) == False
        
    def test_validate_gender(self):
        """
        Test to validate gender
        """
        assert validate_gender(VALID_GENDER) == True

    def test_gender_with_invalid_gender(self):
        """
        Test to validate gender with invalid format
        """
        assert validate_gender(INVALID_GENDER) == False

    def test_validate_password(self):
        """
        Test to validate password
        """
        assert validate_password(VALID_PASSWORD) == True
    
    def test_password_with_invalid_length(self):
        """
        Test to validate password with invalid length
        """
        assert validate_password(INVALID_PASSWORD) == False
    
    def test_validate_username(self):
        """
        Test to validate username
        """
        assert validate_username(VALID_USERNAME) == True
    
    def test_username_with_invalid_format(self):
        """
        Test to validate username with invalid format
        """
        assert validate_username(INVALID_USERNAME) == False
