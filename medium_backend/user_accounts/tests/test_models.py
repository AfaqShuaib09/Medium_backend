'''  Testing of models in user_accounts app  '''
from django.test import TestCase
from user_accounts.tests.constants import PROFILE_CREATION_DATA, USER_DATA
from user_accounts.tests.factories import ProfileFactory, UserFactory


class UserAccountsModelsTestCase(TestCase):
    '''
    Test cases for models in user_accounts app
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.profile = ProfileFactory(user=self.user)
        self.profile.delete()
        self.profile = ProfileFactory.create(
            user = self.user,
            full_name = PROFILE_CREATION_DATA['full_name'],
            bio = PROFILE_CREATION_DATA['bio'],
            cnic = PROFILE_CREATION_DATA['cnic_number'],
            contact_number = PROFILE_CREATION_DATA['contact_number'],
            gender = PROFILE_CREATION_DATA['gender']
        )

    def test_user_model(self):
        '''
        Test for user model
        '''
        self.assertEqual(self.user.username, USER_DATA['username'])
        self.assertEqual(self.user.email, USER_DATA['email'])
        self.assertTrue(self.user.check_password(USER_DATA['password']))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_profile_model(self):
        '''
        Test for profile model
        '''
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.full_name, PROFILE_CREATION_DATA['full_name'])
        self.assertEqual(self.profile.bio, PROFILE_CREATION_DATA['bio'])
        self.assertEqual(self.profile.cnic, PROFILE_CREATION_DATA['cnic_number'])
        self.assertEqual(self.profile.contact_number, PROFILE_CREATION_DATA['contact_number'])
        self.assertEqual(self.profile.gender, PROFILE_CREATION_DATA['gender'])
