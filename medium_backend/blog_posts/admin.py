from django.contrib import admin

from blog_posts.models import Post, Tag, AssignedTag, Comment, Report, Vote

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(AssignedTag)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Vote)
