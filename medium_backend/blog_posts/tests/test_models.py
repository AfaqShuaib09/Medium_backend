from blog_posts.tests.constants import (TAGS, TEST_COMMENT_CONTENT,
                                        TEST_POST_DATA_1)
from blog_posts.tests.factories import (AssignedTagFactory, CommentFactory,
                                        PostFactory, ReportFactory, TagFactory,
                                        VoteFactory)
from django.test import TestCase
from user_accounts.tests.constants import USER_DATA
from user_accounts.tests.factories import UserFactory


class PostModelTestCase(TestCase):
    '''
    Test cases for post model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.post = PostFactory.create(
            posted_by = self.user,
            title = TEST_POST_DATA_1['title'],
            content = TEST_POST_DATA_1['content']
        )
    
    def test_post_model(self):
        '''
        Test for post model
        '''
        self.assertEqual(self.post.posted_by, self.user)
        self.assertEqual(self.post.title, TEST_POST_DATA_1['title'])
        self.assertEqual(self.post.content, TEST_POST_DATA_1['content'])
        self.assertTrue(self.post.created)
        self.assertTrue(self.post.modified)
        self.assertEqual(self.post.total_votes, 0)
    
    def test_post_model_str(self):
        '''
        Test for post model str method
        '''
        self.assertEqual(str(self.post), f'Post: {self.post.title}')
    
    def test_upvote_post(self):
        '''
        Test for upvoting post
        '''
        self.post.upvote(self.user)
        self.assertEqual(self.post.total_votes, 1)
    
    def test_downvote_post(self):
        '''
        Test for downvoting post
        '''
        self.post.downvote(self.user)
        self.assertEqual(self.post.total_votes, -1)
    
    def test_unvote_post(self):
        '''
        Test for devoting post
        '''
        unvote = self.post.unvote(self.user)
        self.assertEqual(unvote, 'You have not voted this post')
        self.assertEqual(self.post.total_votes, 0)


class TagModelTestCase(TestCase):
    '''
    Test cases for tag model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.tags_list = TAGS.split(',')
        self.tags = list()
        for tag in self.tags_list:
            self.tags.append(TagFactory.create(name=tag))
    
    def test_tags_model(self):
        '''
        Test for tags model
        '''
        index = 0
        for tag in self.tags:
            self.assertEqual(tag.name, self.tags_list[index])
            self.assertTrue(tag.created)
            self.assertTrue(tag.modified)
            index += 1
    
    def test_tags_model_str(self):
        '''
        Test for tags model str method
        '''
        index = 0
        for tag in self.tags:
            self.assertEqual(str(tag), f'{self.tags_list[index]}')
            index += 1


class AssignedTagModelTestCase(TestCase):
    '''
    Test cases for assigned tag model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.post = PostFactory.create(
            posted_by = self.user,
            title = TEST_POST_DATA_1['title'],
            content = TEST_POST_DATA_1['content']
        )
        self.tags_list = TAGS.split(',')
        self.tags = list()
        for tag in self.tags_list:
            self.tags.append(TagFactory.create(name=tag))
        self.assigned_tags = list()
        for tag in self.tags:
            self.assigned_tags.append(AssignedTagFactory.create(post=self.post, tag=tag))
    
    def test_assigned_tags_model(self):
        '''
        Test for assigned tags model
        '''
        index = 0
        for assigned_tag in self.assigned_tags:
            self.assertEqual(assigned_tag.post, self.post)
            self.assertEqual(assigned_tag.tag, self.tags[index])
            index += 1
    
    def test_assigned_tags_model_str(self):
        '''
        Test for assigned tags model str method
        '''
        index = 0
        for assigned_tag in self.assigned_tags:
            self.assertEqual(str(assigned_tag), f'{self.post.title} - {self.tags_list[index]}')
            index += 1


class ReportModelTestCase(TestCase):
    '''
    Test cases for report model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.post = PostFactory.create(
            posted_by = self.user,
            title = TEST_POST_DATA_1['title'],
            content = TEST_POST_DATA_1['content']
        )
        self.report = ReportFactory.create(
            reported_by = self.user,
            post = self.post,
            type = 'spam'
        )
    
    def test_report_model(self):
        '''
        Test for report model
        '''
        self.assertEqual(self.report.reported_by, self.user)
        self.assertEqual(self.report.post, self.post)
        self.assertTrue(self.report.created)
        self.assertTrue(self.report.modified)
    
    def test_report_model_str(self):
        '''
        Test for report model str method
        '''
        self.assertEqual(str(self.report), f'Report Type: {self.report.type}, Post: {self.post.title}')


class CommentModelTestCase(TestCase):
    '''
    Test cases for comment model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.post = PostFactory.create(
            posted_by = self.user,
            title = TEST_POST_DATA_1['title'],
            content = TEST_POST_DATA_1['content']
        )
        self.comment = CommentFactory.create(
            owner = self.user,
            post = self.post,
            content = TEST_COMMENT_CONTENT
        )
    
    def test_comment_model(self):
        '''
        Test for comment model
        '''
        self.assertEqual(self.comment.owner, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.content, TEST_COMMENT_CONTENT)
        self.assertTrue(self.comment.created)
        self.assertTrue(self.comment.modified)
    
    def test_comment_model_str(self):
        '''
        Test for comment model str method
        '''
        self.assertEqual(str(self.comment), f'Comment: {self.comment.content[:20]}')
    
    def test_parent_comment(self):
        '''
        Test to check if parent comment is set correctly
        '''
        self.assertEqual(self.comment.is_parent, True)
    
    def test_child_comment(self):
        '''
        Test to check if child comment is set correctly
        '''
        child_comment = CommentFactory.create(
            parent = self.comment,
            owner = self.user,
            post = self.post,
            content = TEST_COMMENT_CONTENT,
        )
        self.assertEqual(child_comment.is_parent, False)
        self.assertEqual(child_comment.parent, self.comment)
    

class PostVoteModelTestCase(TestCase):
    '''
    Test cases for post vote model
    '''
    def setUp(self):
        '''  Setup for test cases  '''
        self.user = UserFactory(
            username = USER_DATA['username'],
            password = USER_DATA['password'], 
            email = USER_DATA['email']
        )
        self.post = PostFactory.create(
            posted_by = self.user,
            title = TEST_POST_DATA_1['title'],
            content = TEST_POST_DATA_1['content']
        )
        self.post_vote = VoteFactory.create(
            user = self.user,
            post = self.post,
            u_vote = True
        )
    
    def test_post_vote_model(self):
        '''
        Test for post vote model
        '''
        self.assertEqual(self.post_vote.user, self.user)
        self.assertEqual(self.post_vote.post, self.post)
        self.assertEqual(self.post_vote.u_vote, True)
        self.assertTrue(self.post_vote.created)
        self.assertTrue(self.post_vote.modified)
