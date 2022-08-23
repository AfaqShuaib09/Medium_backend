from django.contrib import admin

from blog_posts.models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at')

admin.site.register(Post, PostAdmin)
