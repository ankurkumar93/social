from datetime import datetime
from email.policy import default
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, default="name")
    email = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.email


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, default='title')
    desc = models.TextField(default='desc')
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return str(self.id)


class UserFollower(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followee')

    def __str__(self):
        return str(self.id)

    
class LikePost(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


class CommentPost(models.Model):
    id = models.AutoField(primary_key=True)
    comment_text = models.TextField(default="nice post")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


