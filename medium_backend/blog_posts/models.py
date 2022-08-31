""" Models declaration for the blog_posts api """
from django.contrib.auth.models import User
from django.db import models

from blog_posts.constant import REPORT_CHOICES, STATUS_CHOICES


# Create your models here.
class Post(models.Model):
    """ Blog Post Model """
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/posts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isBlocked = models.BooleanField(default=False)

    def __str__(self):
        """ Overrides the str method to return the title of the post """
        return f'Post: {self.title}'

    class Meta:
        """ Meta class defined to set the ordering of the posts """
        ordering = ['-created_at']

    @property
    def total_votes(self):
        """
        Differentiates between upvotes and downvotes
        """
        return self.post_votes.filter(u_vote=True).count() - self.post_votes.filter(u_vote=False).count()

    def upvote(self, user):
        """
        upvote the post
        """
        vote, created = self.post_votes.get_or_create(user=user, post=self)
        if not created and vote.u_vote == True:
            return 'Already up voted this post'

        vote.u_vote = True
        vote.save()
        return 'Successfully up voted this post'

    def downvote(self, user):
        """
        downvote the post
        """
        vote, created = self.post_votes.get_or_create(user=user, post=self)
        if not created and not vote.u_vote:
            return 'Already down voted this post'

        vote.u_vote = False
        vote.save()
        return 'Successfully down voted this post'

    def unvote(self, user):
        """
        Performs Unvote Action
        """
        vote, created = self.post_votes.get_or_create(user=user, post=self)
        if not created:
            vote.delete()
            return 'Successfully unvoted this post'
        return 'You have not voted this post'


class Tag(models.Model):
    """ Model to store the tags """
    name = models.CharField(max_length=20)

    def __str__(self):
        """ display the name of the tag """
        return f'{self.name}'


class AssignedTag(models.Model):
    """ Model to store the tags associated with the post """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='assigned_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='assigned_tags')

    def __str__(self):
        return f'{self.post.title} - {self.tag.name}'


class Comment(models.Model):
    """ Model to save data of Comments on Blog Posts."""
    parent = models.ForeignKey('self', blank=True, null=True, related_name='reply', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=50000)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, related_name='comment',
        on_delete=models.CASCADE, null=True
    )

    def children(self):
        """
        Returns the children of a comment.
        """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """ Checks whether a Comment is a Parent Comment. """
        return False if self.parent else True


class Report(models.Model):
    """ Model to store complaints/reports on posts. """
    type = models.CharField(max_length=50, choices=REPORT_CHOICES, default='spam')
    post = models.ForeignKey(Post, related_name='reports', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Report Type: {self.type}, Post: {self.post.title}'

    class Meta:
        """
        Meta class for unique_together relationship.
        """
        unique_together = ('post', 'reported_by')


class Vote(models.Model):
    """ Model to save data of Votes on Blog Posts. """
    u_vote = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='user_votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_votes', on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for unique_together relationship.
        """
        unique_together = ('user', 'post')

    def __str__(self):
        return f'vote: {self.user.username} - {self.post.title}'
