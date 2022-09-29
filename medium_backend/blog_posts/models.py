""" Models declaration for the blog_posts api """
from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from blog_posts.constant import REPORT_CHOICES, STATUS_CHOICES

# Create your models here.
class Post(TimeStampedModel):
    """ Blog Post Model """
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/posts/', blank=True)
    isBlocked = models.BooleanField(default=False)

    def __str__(self):
        """ Overrides the str method to return the title of the post """
        return f'{self.title}'
    
    class Meta:
        """ Meta subclass to define ordering. """
        ordering = ['-created']

    @property
    def total_votes(self):
        """
        Differentiates between upvotes and downvotes
        """
        return self.post_votes.filter(upvote=True).count() - self.post_votes.filter(upvote=False).count()

    def upvote(self, user):
        """
        upvote the post
        """
        vote, created = self.post_votes.get_or_create(user=user, post=self)
        if not created and vote.upvote == True:
            return 'Already up voted this post'

        vote.upvote = True
        vote.save()
        return 'Successfully up voted this post'

    def downvote(self, user):
        """
        downvote the post
        """
        vote, created = self.post_votes.get_or_create(user=user, post=self)
        if not created and not vote.upvote:
            return 'Already down voted this post'

        vote.upvote = False
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


class Tag(TimeStampedModel):
    """ Model to store the tags """
    name = models.CharField(max_length=20)

    def __str__(self):
        """ display the name of the tag """
        return f'{self.name}'


class AssignedTag(TimeStampedModel):
    """ Model to store the tags associated with the post """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='assigned_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='assigned_tags')

    def __str__(self):
        return f'{self.post.title} - {self.tag.name}'


class Comment(TimeStampedModel):
    """ Model to save data of Comments on Blog Posts."""
    parent = models.ForeignKey('self', blank=True, null=True, related_name='reply', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    content = models.TextField(max_length=50000)
    owner = models.ForeignKey(
        User, related_name='comment',
        on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        """ Overrides the str method to return the content of the comment """
        return self.content[:20]

    def children(self):
        """
        Returns the children of a comment.
        """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """ Checks whether a Comment is a Parent Comment. """
        return False if self.parent else True


class Report(TimeStampedModel):
    """ Model to store complaints/reports on posts. """
    type = models.CharField(max_length=50, choices=REPORT_CHOICES, default='spam')
    post = models.ForeignKey(Post, related_name='reports', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, related_name='reports', on_delete=models.CASCADE)

    def __str__(self):
        return f'Report Type: {self.type}, Post: {self.post.title}, Reported by: {self.reported_by.username}'

    class Meta:
        """
        Meta class for unique_together relationship.
        """
        unique_together = ('post', 'reported_by')


class Vote(TimeStampedModel):
    """ Model to save data of Votes on Blog Posts. """
    upvote = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='user_votes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_votes', on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for unique_together relationship.
        """
        unique_together = ('user', 'post')

    def __str__(self):
        return f'vote: {self.user.username} - {self.post.title}'
