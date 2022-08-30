import os

from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase
from user_accounts.models import Profile
from user_accounts.tests.constants import (ADMIN_CREDENTIALS, INVALID_CNIC,
                                           INVALID_CONTACT_NO, INVALID_GENDER,
                                           LOGIN_TEST_USER_DATA, NEW_PASSWORD,
                                           PROFILE_CREATION_DATA,
                                           REGISTER_TEST_USER_DATA, USER_DATA)
from user_accounts.validators import validate_file_extension
from user_accounts.views import (ChangePasswordViewSet, ProfileViewSet,
                                 UserViewSet)


# Create your tests here.
class RegisterTest(APITestCase):
    """ Test registration endpoint by giving credentials for test purposes """

    def setUp(self):
        """ intiaitilize the request factory and the data to be sent in the request and before each test """
        self.register_url = '/api/register/'
        self.data = REGISTER_TEST_USER_DATA
        return super().setUp()

    def tearDown(self):
        """ Clean up the test database after each test """
        return super().tearDown()

    def test_register_success(self):
        """
        Test that a post request to the register view creates a new user.
        """
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')
        self.assertEqual(User.objects.get().email, 'test@test.com')

    def test_register_with_already_existing_user(self):
        """
        Test that a register request with an already existing user
        """
        User.objects.create(username='test', email ='test@test.com', password='testqweasd')
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_user_cannot_register_without_username(self):
        """
        user fails to register without a username.
        """
        self.data.pop('username')
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_cannot_register_without_email(self):
        """
        user fails to register without an email
        """
        self.data.pop('email')
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_register_with_invalid_email(self):
        """
        user fails to register with an invalid email
        """
        self.data['email'] = 'test#test.com'
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_cannot_register_with_weak_password(self):
        """
        Test that a user cannot register with a weak password
        """
        self.data['password'] = 'test'
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_cannot_register_with_invalid_username(self):
        """
        Test that a user cannot register with an invalid username.
        """
        self.data['username'] = 'test# test'
        response = self.client.post(self.register_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

class LoginTest(APITestCase):
    """ Test the login functionality with given credentials """
    def setUp(self):
        """ Initialize the data before each login test """
        self.login_url = '/api/login/'
        user = User.objects.create(username='test', email ='test@test.com')
        user.set_password('testqweasd')
        user.save()
        self.data = LOGIN_TEST_USER_DATA
        return super().setUp()

    def tearDown(self):
        """ Clean up the test database after each test """
        return super().tearDown()

    def test_login_success(self):
        """ Login the user successfully with the given credentials """
        response = self.client.post(self.login_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_view_post_request_with_invalid_credentials(self):
        """ User fails to login with invalid credentials """
        self.data['password'] = 'testqweasd1'
        response = self.client.post(self.login_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_post_request_with_invalid_username(self):
        """ User fails to login with invalid username """
        self.data['username'] = 'test1'
        response = self.client.post(self.login_url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserTest(APITestCase):
    """ Test the user endpoints """
    factory = APIRequestFactory()
    def setUp(self):
        self.user_url = '/api/users/'
        self.login_url = '/api/login/'
        self.user = User.objects.create_superuser(username=ADMIN_CREDENTIALS['username'],
                                                    email=ADMIN_CREDENTIALS['email'])
        self.user.set_password(ADMIN_CREDENTIALS['password'])
        self.user.save()
        self.token = AuthToken.objects.create(user=self.user)[1]
        return super().setUp()

    def tearDown(self):
        """ Clean up the test database after each test """
        return super().tearDown()

    def test_get_user_all_users(self):
        """ Test that all list all users """
        view = UserViewSet.as_view({
            'get': 'list'
        })
        url = '/api/users/'
        request = self.factory.get(url, HTTP_AUTHORIZATION='Token ' + self.token)
        response = view(request)
        assert status.HTTP_200_OK == response.status_code

    def test_get_user_all_users_with_invalid_token(self):
        """ Test list all users fails with invalid token """
        view = UserViewSet.as_view({
            'get': 'list'
        })
        url = '/api/users/'
        request = self.factory.get(url, HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = view(request)
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_get_user_by_id(self):
        """ Test that a user can be retrieved by id """
        view = UserViewSet.as_view({
            'get': 'retrieve'
        })
        url = '/api/users/1'
        request = self.factory.get(url, HTTP_AUTHORIZATION='Token ' + self.token)
        response = view(request, pk=1)
        assert status.HTTP_200_OK == response.status_code

    def test_get_user_by_id_with_invalid_token(self):
        """ user fails to retrieve a user by id with invalid token """
        view = UserViewSet.as_view({
            'get': 'retrieve'
        })
        url = '/api/users/1'
        request = self.factory.get(url, HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = view(request, pk=1)
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

class UserProfileViewSetTest(APITestCase):
    """ Test the user profile endpoints """
    factory = APIRequestFactory()
    def setUp(self):
        self.user_url = '/api/users/'
        self.login_url = '/api/login/'
        self.user = User.objects.create(username=USER_DATA['username'], email=USER_DATA['email'])
        self.user.set_password(USER_DATA['password'])
        self.user.save()
        self.token = AuthToken.objects.create(user=self.user)[1]
        return super().setUp()

    def tearDown(self):
        """ Clean up the test database after each test """
        return super().tearDown()

    def test_get_all_user_profile(self):
        """ Test to get all user profiles """
        view = ProfileViewSet.as_view({
            'get': 'list'
        })
        url = '/api/profile/'
        request = self.factory.get(f'{url}', HTTP_AUTHORIZATION='Token ' + self.token)
        response = view(request)
        assert status.HTTP_200_OK == response.status_code

    def test_get_all_user_profile_with_invalid_token(self):
        """ Fails to get all user profiles with invalid token """
        view = ProfileViewSet.as_view({
            'get': 'list'
        })
        url = '/api/profile/'
        request = self.factory.get(f'{url}', HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = view(request)
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_get_user_profile_by_username(self):
        """ Test to get a user profile by username """
        view = ProfileViewSet.as_view({
            'get': 'retrieve'
        })
        url = '/api/profile/'
        request = self.factory.get(f'{url}', HTTP_AUTHORIZATION='Token ' + self.token)
        response = view(request, user__username='afaqboi')
        assert status.HTTP_200_OK == response.status_code

    def test_profile_nonexistent_username(self):
        """ Test to get a user profile by username that doesn't exist """
        view = ProfileViewSet.as_view({
            'get': 'retrieve'
        })
        url = '/api/profile/'
        request = self.factory.get(f'{url}', HTTP_AUTHORIZATION='Token ' + self.token)
        response = view(request, user__username='nonexistent_username')
        assert status.HTTP_404_NOT_FOUND == response.status_code

    def test_update_user_profile(self):
        """ Test to update a user profile """
        user = User.objects.get(username='afaqboi')
        profile = Profile.objects.get(user=user)
        update_profile_data = {
            'full_name': 'test full name',
            'bio': 'test bio',
        }
        url = '/api/profile/afaqboi'
        request = self.factory.patch(url, update_profile_data, HTTP_AUTHORIZATION='Token ' + self.token)
        view = ProfileViewSet.as_view({
            'patch': 'partial_update',
        })
        response = view(request, user__username='afaqboi')
        assert status.HTTP_200_OK == response.status_code
        profile.refresh_from_db()
        assert profile.full_name == update_profile_data['full_name']
        assert profile.bio == update_profile_data['bio']
    
    def test_update_user_profile_with_invalid_token(self):
        """ Fails to update a user profile with invalid token """
        user = User.objects.get(username='afaqboi')
        update_profile_data = {
            'full_name': 'test full name',
            'bio': 'test bio',
        }
        url = '/api/profile/afaqboi'
        request = self.factory.put(url, update_profile_data, HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        view = ProfileViewSet.as_view({
            'put': 'update'
        })
        response = view(request, user__username='afaqboi')
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_update_user_profile_with_nonexistent_username(self):
        """ Fails to update a user profile that doesn't exist """
        user = User.objects.get(username='afaqboi')
        profile = Profile.objects.get(user=user)
        update_profile_data = {
            'full_name': 'test full name',
            'bio': 'test bio',
        }
        url = '/api/profile/nonexistent_username'
        request = self.factory.patch(url, update_profile_data, HTTP_AUTHORIZATION='Token ' + self.token)
        view = ProfileViewSet.as_view({
            'patch': 'update'
        })
        response = view(request, user__username='nonexistent_username')
        assert status.HTTP_404_NOT_FOUND == response.status_code

    def test_delete_user_profile(self):
        """ Test to delete a user profile """
        user = User.objects.get(username='afaqboi')
        profile = Profile.objects.get(user=user)
        url = '/api/profile/afaqboi'
        request = self.factory.delete(url, HTTP_AUTHORIZATION='Token ' + self.token)
        view = ProfileViewSet.as_view({
            'delete': 'destroy'
        })
        response = view(request, user__username='afaqboi')
        assert status.HTTP_204_NO_CONTENT == response.status_code
        assert not Profile.objects.filter(user=user).exists()

    def test_delete_user_profile_with_invalid_token(self):
        """ Fails to delete a user profile with invalid token """
        user = User.objects.get(username='afaqboi')
        profile = Profile.objects.get(user=user)
        url = '/api/profile/afaqboi'
        request = self.factory.delete(url, HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        view = ProfileViewSet.as_view({
            'delete': 'destroy'
        })
        response = view(request, user__username='afaqboi')
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_create_user_profile(self):
        """ Test to create a user profile """
        user = User.objects.get(username='afaqboi')
        # delete the profile here because the profile is created on successful registration
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = PROFILE_CREATION_DATA
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_201_CREATED == response.status_code
        assert Profile.objects.filter(user=user).exists()
        assert str(Profile.objects.get(user=user)) == f'{self.user.username} Profile'

    def test_create_user_profile_with_invalid_token(self):
        """ Fails to create a user profile with invalid token """
        # delete the profile here because the profile is created on successful registration
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = PROFILE_CREATION_DATA
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + 'invalid_token', data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_create_user_profile_with_nonexistent_username(self):
        """ Fails to create a user profile with nonexistent username """
        # delete the profile here because the profile is created on successful registration
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = {
            'username': 'nonexistent_username',
            'full_name': 'test full name',
        }
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_404_NOT_FOUND == response.status_code

    def test_create_user_with_invlaid_gender(self):
        """ Fails to create a user profile with invalid gender """
        # delete the profile here because the profile is created on successful registration
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = {
            'username': 'afaqboi',
            'gender': INVALID_GENDER
        }
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_create_user_with_invalid_cnic(self):
        """ Fails to create a user profile with invalid cnic """
        # delete the profile here because the profile is created on successful registration
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = {
            'username': 'afaqboi',
            'cnic': INVALID_CNIC,
        }
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_create_user_with_invalid_contact_number(self):
        """ Test that a user profile cannot be created with an invalid contact number """
        self.test_delete_user_profile()
        url = '/api/profile/'
        data = {
            'username': 'afaqboi',
            'contact_number': INVALID_CONTACT_NO,
        }
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_400_BAD_REQUEST == response.status_code
    
    def test_create_user_profile_with_already_existing_username(self):
        """ Fails to create a user profile with already existing username """
        # delete the profile here because the profile is created on successful registration
        self.test_create_user_profile()
        url = '/api/profile/'
        data = {
            'username': 'afaqboi',
            'full_name': 'test full name',
        }
        request = self.factory.post(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ProfileViewSet.as_view({
            'post': 'create'
        })
        response = view(request)
        assert status.HTTP_400_BAD_REQUEST == response.status_code

class TestChangeUserPassword(APITestCase):
    """ Test the change user password view. """

    def setUp(self):
        """ Set up the test """
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username=USER_DATA['username'], email=USER_DATA['email'])
        self.user.set_password(USER_DATA['password'])
        self.user.save()
        self.token = AuthToken.objects.create(user=self.user)[1]

    def test_change_user_password_success(self):
        """ Test to change user password successfully """
        url = '/api/change-password/'
        data = {
            'old_password': USER_DATA['password'],
            'new_password': NEW_PASSWORD,
        }
        response = self.factory.put(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ChangePasswordViewSet.as_view({
            'put' : 'update'
        })
        response = view(response, pk=self.user.id)
        assert status.HTTP_200_OK == response.status_code

    def test_change_user_password_with_invalid_token(self):
        """ Test to change user password with invalid token """
        url = '/api/change-password/'
        data = {
            'old_password': USER_DATA['password'],
            'new_password': NEW_PASSWORD,
        }
        response = self.factory.put(url, HTTP_AUTHORIZATION='Token ' + 'invalid_token', data=data)
        view = ChangePasswordViewSet.as_view({
            'put' : 'update'
        })
        response = view(response, pk=self.user.id)
        assert status.HTTP_401_UNAUTHORIZED == response.status_code

    def test_change_user_password_with_invalid_old_password(self):
        """ Test to change user password with wrong old password """
        url = '/api/change-password/'
        data = {
            'old_password': 'invalid_password',
            'new_password': NEW_PASSWORD,
        }
        response = self.factory.put(url, HTTP_AUTHORIZATION='Token ' + self.token, data=data)
        view = ChangePasswordViewSet.as_view({
            'put' : 'update'
        })
        response = view(response, pk=self.user.id)
        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_forgot_password_to_print_reset_code(self):
        """ Reset password code is printed on the console """
        response = self.client.post('/api/forgot-password/', data={'email': self.user.email})
        assert status.HTTP_200_OK == response.status_code
