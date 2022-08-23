from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/posts/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    isBlocked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class AssignedTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='assigned_tags')

    def __str__(self):
        return f'{self.post.title} - {self.tag.name}'
