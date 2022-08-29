import email
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from knox.models import AuthToken
from user_accounts.tests import RegisterTest

from blog_posts.models import Post, Tag, AssignedTag, Comment, Report
from blog_posts.views import ReviewReportViewSet
# Create your tests here.
class PostTest(APITestCase):
    """ Test module for Post API """
    def setUp(self):
        """ Set up test variables """
        self.client = APIClient()
        self.req_factory = APIRequestFactory()
        user = User.objects.create_user(username='test_user', email='test@test.com')
        user.set_password('test_password')
        user.save()
        self.credentials = {
            'username': 'test_user',
            'password': 'test_password'
        }
        self.token = AuthToken.objects.create(user)[1]
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
        }
        self.post_data_2 = {
            'title': 'Test Post 2',
            'content': 'Test Content 2',
            'tags': 'Test_Tag,news,sports',
        }

    def test_create_post(self):
        """ Test create post endpoint """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/posts/', self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.post_data['title'])
        self.assertEqual(response.data['content'], self.post_data['content'])

    def test_create_post_with_tags(self):
        """ Test create post with tags """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post('/api/posts/', self.post_data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.post_data_2['title'])
        self.assertEqual(response.data['content'], self.post_data_2['content'])
        tags_list = self.post_data_2['tags'].split(',')
        for tag in tags_list:
            assigned_tags  = AssignedTag.objects.get(tag__name=tag, post=response.data['id'])
            self.assertEqual(assigned_tags.tag.name, tag)

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
        post = Post.objects.get(title=self.post_data['title'])
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
        post = Post.objects.get(title=self.post_data['title'])
        updated_data = {
            'title': 'Test Post Updated',
            'content': 'Test Content Updated',
        }
        response = self.client.put(f'/api/posts/{post.id}/',data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post Updated')
        self.assertEqual(response.data['content'], 'Test Content Updated')

    def test_update_post_with_invalid_id(self):
        """ Fails to update post with invalid id """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put('/api/posts/1/', format='json')
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
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.delete(f'/api/posts/{post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(title=self.post_data['title']).count(), 0)

    def test_delete_post_with_invalid_token(self):
        """ Fails to delete post with invalid token """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.delete('/api/posts/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_posts_with_valid_query(self):
        """ Test to search posts with valid query """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        response = self.client.get('/api/posts/?search=Test', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Post')

    def test_search_posts_with_tags(self):
        """ Test to search posts with tags query """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post_with_tags()
        response = self.client.get('/api/posts/?search_fields=assigned_tags__tag__name&search=news', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.post_data_2['title'])

    def test_post_upvote_success(self):
        """ Test the upvote post functionality """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/upvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully up voted this post'

    def test_post_upvote_already_upvoted(self):
        """ Test to check post already upvoted """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_post_upvote_success()
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/upvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Already up voted this post'

    def test_post_downvote_success(self):
        """ Test the post downvote functionality """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/downvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully down voted this post'

    def test_post_downvote_already_downvoted(self):
        """ Test to check post already downvoted """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_post_downvote_success()
        post = Post.objects.get(title=self.post_data['title'])
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
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'Successfully unvoted this post'

    def test_post_unvoted_non_voted_post(self):
        """ Test to unvote the non voted post """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_post()
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data == 'You have not voted this post'

    def test_post_unvote_with_invalid_token(self):
        """ Test post unvote with invalid token unauthenticated """
        self.test_post_upvote_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        post = Post.objects.get(title=self.post_data['title'])
        response = self.client.get(f'/api/posts/{post.id}/unvote/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CommentTest(APITestCase):
    """ Test Comment API """
    def setUp(self):
        """ Set up test data """
        self.user = User.objects.create_user(username='test', email='test@test.com')
        self.user.set_password('asdqweasd')
        self.token = AuthToken.objects.create(user=self.user)[1]
        post = PostTest()
        post.setUp()
        post.test_create_post_with_tags()
        post.test_create_post()
        self.post_data = {
            'title': 'Test Post',
            'content': 'Test Content',
        }
        self.post_data_2 = {
            'title': 'Test Post 2',
            'content': 'Test Content 2',
        }
        self.post_1 = Post.objects.get(title=post.post_data['title'])
        self.post_2 = Post.objects.get(title=post.post_data_2['title'])
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
        comment = Comment.objects.get(content=self.comment_data['content'])
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
        comment = Comment.objects.get(content=self.comment_data['content'])
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
        comment = Comment.objects.get(content=self.comment_data['content'])
        response = self.client.put(f'/api/comment/{comment.id}/', self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_delete_success(self):
        """ Test to delete comment """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.test_create_comment_success()
        comment = Comment.objects.get(content=self.comment_data['content'])
        response = self.client.delete(f'/api/comment/{comment.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_post_comments(self):
        """ Test to get all post comments """
        self.test_create_comment_success()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'/api/post_comment/?post={self.post_1.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1


class ReportTest(APITestCase):
    """ Test Report API """
    def setUp(self):
        """ Set up test data """
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email = 'test@test.com')
        self.user.set_password('asdqweasd')
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
        self.post_1 = Post.objects.create(**self.post_data)
        self.post_2 = Post.objects.create(**self.post_data_2)
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

    def test_create_report_with_invalid_type(self):
        """ Test to report post with invalid type """
        self.report_data['type'] = 'invalid_type'
        response = self.client.post('/api/reports/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        self.assertEqual(response.data[0].get('reported_by')['id'], self.user.id)

    def test_update_report_success(self):
        """ Test to edit the report """
        self.test_create_report_success()
        report = Report.objects.get(post=self.post_1.id)
        self.report_data['type'] = 'hate-speech'
        response = self.client.put(f'/api/reports/{report.id}/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data['type'] == 'Hate Speech and Symbol used'

    def test_update_report_with_invalid_token(self):
        """ Test update report with invalid authentication token """
        self.test_create_report_success()
        report = Report.objects.get(post=self.post_1.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'invalid_token')
        response = self.client.put(f'/api/reports/{report.id}/', self.report_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_report_success(self):
        """ Test to delete report """
        self.test_create_report_success()
        report = Report.objects.get(post=self.post_1.id)
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
        report = Report.objects.filter(post=self.post_1.id).first()
        review_data = {
            'status': 'approved',
        }
        response = self.client.patch(f'/api/review_reports/{report.id}', data=review_data, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_report_success(self):
        """ Test review report success by a superuser (admin) """
        req_factory = APIRequestFactory()
        self.test_create_report_success()
        report = Report.objects.filter(post=self.post_1.id).first()
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


class VoteTest(APITestCase):
    """ Test Vote API """
    def setUp(self):
        """ Set up test data """
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', email = 'test@test.com')
        self.user.set_password('asdqweasd')
        self.token = AuthToken.objects.create(user=self.user)[1]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        post_test = PostTest()
        post_test.setUp()
        post_test.test_post_upvote_success()
        post_test.test_create_post_with_tags()
        self.post = Post.objects.get(title='Test Post')

    def test_get_all_votes_success(self):
        """ Test to get all votes """
        response = self.client.get('/api/votes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1

    def test_get_vote_success(self):
        """ Test to get all post votes """
        response = self.client.get(f'/api/votes/?post={self.post.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1
