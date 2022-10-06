from django.contrib import admin
from .models import User, UserFollower, Post, LikePost, CommentPost

admin.site.register(User)
admin.site.register(UserFollower)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(CommentPost)
