from curses import keyname
from blog_posts.models import AssignedTag, Comment, Post, Report, Vote
from blog_posts.tests.constants import (TEST_LOGIN_CREDENTIALS,
                                        TEST_POST_DATA_1, TEST_POST_DATA_2,
                                        TEST_UPDATE_POST_DATA,
                                        TEST_UPDATE_POST_DATA_2,
                                        TEST_UPDATE_POST_DATA_3,
                                        TEST_USER_DATA)
from blog_posts.views import ReviewReportViewSet
from django.contrib.auth.models import User
from user_accounts.tests.test_factories import UserFactory
from blog_posts.tests.test_factories import PostFactory, TagFactory, AssignedTagFactory, VoteFatory, CommentFactory, ReportFactory
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase


# Create your tests here.
class PostTest(APITestCase):
    """ Test module for Post API """
    def setUp(self):
        """ Set up test variables """
        self.client = APIClient()
        self.req_factory = APIRequestFactory()
        self.user = UserFactory(**TEST_USER_DATA)
        self.credentials = TEST_LOGIN_CREDENTIALS
        self.token = AuthToken.objects.create(self.user)[1]
        self.post_data = TEST_POST_DATA_1
        self.post_data_2 = TEST_POST_DATA_2

    def test_create_post(self):
        """ Test create post endpoint """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/posts/', self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])
        assert str(PostFactory(title=response.data['title'], posted_by=self.user)) == f'Post: {self.post_data["title"]}'

    def test_create_post_with_tags(self):
        """ Test create post with tags """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/posts/', self.post_data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.post_data_2['title'])
        self.assertEqual(response.data['content'], self.post_data_2['content'])
        tags_list = self.post_data_2['tags'].split(',')
        for tag in tags_list:
            assigned_tags = AssignedTagFactory(tag=TagFactory(name=tag),
                                            post=PostFactory(title=self.post_data_2['title'], posted_by=self.user))
            self.assertEqual(assigned_tags.tag.name, tag)
            assert str(assigned_tags.tag) == f'{tag}'
            assert str(assigned_tags) == f'{self.post_data_2["title"]} - {tag}'

    def test_create_post_with_invalid_token(self):
        """ Fail to create post with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.post('/api/posts/', self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_with_no_data(self):
        """ Fails to create post with no data """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/posts/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_posts(self):
        """ Test to list all posts """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_posts_with_invalid_token(self):
        """ Fails to list all posts with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.get('/api/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_posts_with_no_token(self):
        """ Fail to list all posts with no token """
        response = self.client.get('/api/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_with_valid_id(self):
        """ Test to get post by id """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.post_data['title'])

    def test_get_post_with_invalid_id(self):
        """ Fail to get post with invalid id """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/posts/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_with_invalid_token(self):
        """ Fail to get post with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.get('/api/posts/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_sucess(self):
        """ Test to update post successfully """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        updated_data = TEST_UPDATE_POST_DATA
        response = self.client.put(f'/api/posts/{post.id}/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], TEST_UPDATE_POST_DATA['title'])
        self.assertEqual(response.data['content'], TEST_UPDATE_POST_DATA['content'])

    def test_update_post_by_adding_tags(self):
        """ Test to update post by change tag """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post_with_tags()
        post = PostFactory(title=self.post_data_2['title'], posted_by=self.user)
        updated_data = TEST_UPDATE_POST_DATA_2
        response = self.client.put(f'/api/posts/{post.id}/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], TEST_UPDATE_POST_DATA_2['title'])
        self.assertEqual(response.data['content'], TEST_UPDATE_POST_DATA_2['content'])
        tags_list = TEST_UPDATE_POST_DATA_2['tags'].split(',')
        for tag in tags_list:
            assigned_tags = AssignedTagFactory(tag=TagFactory(name=tag), post=post)
            self.assertEqual(assigned_tags.tag.name, tag)

    def test_update_post_by_removing_all_tags(self):
        """ Test to update post by removing all tags """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post_with_tags()
        post = PostFactory(title=self.post_data_2['title'], posted_by=self.user)
        updated_data = TEST_UPDATE_POST_DATA_3
        response = self.client.put(f'/api/posts/{post.id}/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], TEST_UPDATE_POST_DATA_3['title'])
        self.assertEqual(response.data['content'], TEST_UPDATE_POST_DATA_3['content'])

    def test_update_post_with_invalid_id(self):
        """ Fails to update post with invalid id """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        updated_data = TEST_UPDATE_POST_DATA
        response = self.client.put('/api/posts/1/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_with_invalid_token(self):
        """ Fails to update post with invalid token unauthorized """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.put('/api/posts/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_success(self):
        """ Test to delete post successfully """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.delete(f'/api/posts/{post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(title=self.post_data['title'], posted_by=self.user).count(), 0)

    def test_delete_post_with_invalid_token(self):
        """ Fails to delete post with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.delete('/api/posts/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_posts_with_valid_query(self):
        """ Test to search posts with valid query """
        keyword = 'Test'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        response = self.client.get(f'/api/posts/?search={keyword}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            assert (keyword in response.data[0]['title'])

    def test_search_posts_with_tags(self):
        """ Test to search posts with tags query """
        search_keyword = 'news'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post_with_tags()
        response = self.client.get(f'/api/posts/?search_fields=assigned_tags__tag__name&search={search_keyword}',
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check the searched tag posts is in the response
        found = False
        if response.data:
            for post in response.data:
                for tag in post['assigned_tags']:
                    if tag['name'] == search_keyword:
                        found = True
                        break
        else:
            found = True
        self.assertTrue(found)

    def test_post_upvote_success(self):
        """ Test the upvote post functionality """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/upvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully up voted this post'
        assert str(VoteFatory(post=post, user=self.user)) == f'vote: {self.user.username} - {post.title}'

    def test_post_upvote_already_upvoted(self):
        """ Test to check post already upvoted """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_post_upvote_success()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/upvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Already up voted this post'

    def test_post_downvote_success(self):
        """ Test the post downvote functionality """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/downvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully down voted this post'

    def test_post_downvote_already_downvoted(self):
        """ Test to check post already downvoted """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_post_downvote_success()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/downvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Already down voted this post'

    def test_post_upvote_with_invalid_id(self):
        """ Test to upvote non existing post """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get('/api/posts/1/upvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_unvote_success(self):
        """ Test to check post unvote functionality """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_post_upvote_success()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully unvoted this post'

    def test_post_unvoted_non_voted_post(self):
        """ Test to unvote the non voted post """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'You have not voted this post'

    def test_post_unvote_with_invalid_token(self):
        """ Test post unvote with invalid token unauthenticated """
        self.test_post_upvote_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        post = PostFactory(title=self.post_data['title'], posted_by=self.user)
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CommentTest(APITestCase):
    """ Test Comment API """
    def setUp(self):
        """ Set up test data """
        post = PostTest()
        post.setUp()
        post.test_create_post_with_tags()
        post.test_create_post()
        self.post_data = TEST_POST_DATA_1
        self.post_data_2 = TEST_POST_DATA_2
        self.user = UserFactory(username=TEST_USER_DATA['username'])
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.post_1 = PostFactory(title=post.post_data['title'], posted_by=self.user)
        self.post_2 = PostFactory(title=post.post_data_2['title'], posted_by=self.user)
        self.comment_data = {
            'content': 'Test Comment',
            'post': self.post_1.id,
        }

    def test_create_comment_success(self):
        """ Test to create comment successfully """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/comment/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.data['content'] == self.comment_data['content']

    def test_create_reply_success(self):
        """ Test to add reply to comment successfully """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_comment_success()
        comment = CommentFactory(content=self.comment_data['content'], post=self.post_1, owner=self.user)
        self.reply_data = {
            'parent': comment.id,
            'content': 'Reply to comment',
            'post': self.post_1.id,
        }
        response = self.client.post('/api/comment/', self.reply_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.data['content'] == 'Reply to comment'

    def test_comment_with_invalid_post(self):
        """ Test to comment on non existing post """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.comment_data['post'] = 5
        response = self.client.post('/api/comment/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_with_invalid_token(self):
        """ Test to comment with invalid token unauthenticated """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.post('/api/comment/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_update_success(self):
        """ Test to update comment """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_comment_success()
        comment = CommentFactory(content=self.comment_data['content'], post=self.post_1, owner=self.user)
        self.comment_data['content'] = 'Updated comment'
        response = self.client.put(f'/api/comment/{comment.id}/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data['content'] == 'Updated comment'

    def test_update_non_existent_comment(self):
        """ Test to update non existing comment """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put('/api/comment/1/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_comment_with_invalid_token(self):
        """ Test to update comment with invalid auth token """
        self.test_create_comment_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        comment = CommentFactory(content=self.comment_data['content'], post=self.post_1, owner=self.user)
        response = self.client.put(f'/api/comment/{comment.id}/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete_success(self):
        """ Test to delete comment """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_comment_success()
        comment = CommentFactory(content=self.comment_data['content'], post=self.post_1, owner=self.user)
        response = self.client.delete(f'/api/comment/{comment.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_post_comments(self):
        """ Test to get all post comments """
        search_post = self.post_1.id
        self.test_create_comment_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'/api/post_comment/?post={search_post}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            for comment in response.data:
                assert comment['post'].get('id') == self.post_1.id


class ReportTest(APITestCase):
    """ Test Report API """
    def setUp(self):
        """ Set up test data """
        self.client = APIClient()
        self.user = UserFactory(username=TEST_USER_DATA['username'],
                                email=TEST_USER_DATA['email'], password=TEST_USER_DATA['password'])
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
            'posted_by': self.user,
        }
        self.post_data_2 = {
            'title': 'Test Post 2',
            'content': 'Test Content 2',
            'posted_by': self.user,
        }
        self.post_1 = PostFactory(**self.post_data)
        self.post_2 = PostFactory(**self.post_data_2)
        self.report_data = {
            'post': self.post_1.id,
            'type': 'spam',
            'reported_by': self.user.id,
        }

    def test_create_report_success(self):
        """ Test to report post successfully """
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.data['type'] == 'It\'s spam'
        assert str(ReportFactory(reported_by=self.user, post=self.post_1)) == ('Report Type: spam,'
                                                                                + f' Post: {self.post_1.title}')

    def test_report_already_reported_post(self):
        """ Test to report already reported post """
        self.test_create_report_success()
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_invalid_type(self):
        """ Test to report post with invalid type """
        self.report_data['type'] = 'invalid_type'
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_report_with_admin_user(self):
        """ Test to get all reports with admin user """
        self.test_create_report_success()
        super_user = UserFactory(username='admin', email='admin@admin.com',
                                    password='admin2327', is_superuser=True, is_staff=True)
        token = AuthToken.objects.create(user=super_user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/reports/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_report_with_invalid_post(self):
        """ Test to report non existing post """
        self.report_data['post'] = 5
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_report_with_invalid_token(self):
        """ Test create report with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_report_success(self):
        """ Test to get all reports reported by user """
        self.test_create_report_success()
        response = self.client.get('/api/reports/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data:
            for report in response.data:
                assert report['reported_by'].get('id') == self.user.id

    def test_update_report_success(self):
        """ Test to edit the reports """
        self.test_create_report_success()
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        self.report_data['type'] = 'hate-speech'
        response = self.client.put(f'/api/reports/{report.id}/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data['type'] == 'Hate Speech and Symbol used'

    def test_update_report_with_invalid_token(self):
        """ Test update report with invalid authentication token """
        self.test_create_report_success()
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.put(f'/api/reports/{report.id}/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_report_success(self):
        """ Test to delete report """
        self.test_create_report_success()
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        response = self.client.delete(f'/api/reports/{report.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_report(self):
        """ Test to delete non existing report """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete('/api/reports/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_report_fails(self):
        """ Fails to review report by a simple user """
        self.test_create_report_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        review_data = {
            'status': 'approved',
        }
        response = self.client.patch(f'/api/review_reports/{report.id}', data=review_data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_report_success(self):
        """ Test review report success by a superuser (admin) """
        req_factory = APIRequestFactory()
        self.test_create_report_success()
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        super_user = User.objects.create_superuser(username='admin', email='admin@admin.com')
        super_user.set_password('admin123')
        super_user.save()
        view = ReviewReportViewSet.as_view({
            'patch': 'update'
        })
        token = AuthToken.objects.create(user=super_user)[1]
        review_data = {
            'status': 'approved',
        }
        # use request factory because client.patch not handle redirection correctly
        request = req_factory.patch(f'/api/review_reports/{report.id}', data=review_data,
                                    HTTP_AUTHORIZATION='Token ' + token)
        response = view(request, pk=report.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_report_by_invalid_status(self):
        """ Test review report by invalid status """
        req_factory = APIRequestFactory()
        self.test_create_report_success()
        report = ReportFactory(post=self.post_1, reported_by=self.user)
        super_user = User.objects.create_superuser(username='admin', email='admin@admin.com')
        super_user.set_password('admin123')
        super_user.save()
        view = ReviewReportViewSet.as_view({
            'patch': 'update'
        })
        token = AuthToken.objects.create(user=super_user)[1]
        review_data = {
            'status': 'no-status',
        }
        # use request factory because client.patch not handle redirection correctly
        request = req_factory.patch(f'/api/review_reports/{report.id}', data=review_data,
                                    HTTP_AUTHORIZATION='Token ' + token)
        response = view(request, pk=report.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VoteTest(APITestCase):
    """ Test Vote API """
    def setUp(self):
        """ Set up test data """
        self.client = APIClient()
        self.user = UserFactory()
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        post_test = PostTest()
        post_test.setUp()
        post_test.test_post_upvote_success()
        post_test.test_create_post_with_tags()
        self.post = PostFactory(title='Test Post', posted_by=self.user)

    def test_get_all_votes_success(self):
        """ Test to get all votes """
        response = self.client.get('/api/votes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_post_vote_success(self):
        """ Test to get all post votes of the passed post id """
        response = self.client.get(f'/api/votes/?post={self.post.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for vote in response.data:
            self.assertEqual(vote['post'], self.post.id)
