""" Test Data to be used in testing of endpoints related to blog posts """

TEST_USER_DATA = {
    'username': 'test_user',
    'password': 'test_password',
    'email': 'test@test.com'
}
TEST_LOGIN_CREDENTIALS = {
    'username': 'test_user',
    'password': 'test_password'
}
TEST_POST_DATA_1 = {
    'title': 'Test Post',
    'content': 'Test Content',
}
TEST_POST_DATA_2 = {
    'title': 'Test Post 2',
    'content': 'Test Content 2',
    'tags': 'Test_Tag,news,sports',
}
TEST_UPDATE_POST_DATA = {
    'title': 'Updated Test Post',
    'content': 'Updated Test Content',
}

TEST_UPDATE_POST_DATA_2 = {
    'title': 'Updated Test Post 2',
    'content': 'Updated Test Content 2',
    'tags': 'update-tag,news,sports',
}

TEST_UPDATE_POST_DATA_3 = {
    'title': 'Test Post 3',
    'content': 'Test Content 3',
    'tags': '',
}
