from django.contrib import admin
from feed.models import Follow, Like, Post, Comment, CommentReply
# Register your models here.

admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentReply)