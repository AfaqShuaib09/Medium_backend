""" Test Data to be used in the User Accounts Tests """
REGISTER_TEST_USER_DATA = {
    'username': 'test',
    'password': 'testqweasd',
    'email': 'test@test.com'
}

LOGIN_TEST_USER_DATA = {
    'username': 'test',
    'password': 'testqweasd'
}

ADMIN_CREDENTIALS = {
    'username': 'test_admin',
    'email': 'adminboi@admin.com',
    'password': 'admin1234'
}

USER_DATA = {
    'username': 'afaqboi',
    'email': 'afaq.shoaib09@gmail.com',
    'password': 'afaq2327'
}

PROFILE_CREATION_DATA = {
    'username': 'afaqboi',
    'full_name': 'Afaq Shoaib',
    'bio': 'I am a software developer',
    'gender': 'Male',
    'cnic_number' : '35202-2567944-3',
    'contact_number' : '+923064416475'
}

TEST_PROFILE_UPDATE_DATA = {
    'full_name': 'test full name',
    'bio': 'test bio',
}

INVALID_GENDER = 'in'
INVALID_CNIC = '1234-56789-0125'
INVALID_CONTACT_NO = '+9230644164'
NEW_PASSWORD = 'new_password'
