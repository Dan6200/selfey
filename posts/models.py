from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()


class Post (models.Model):
    image = models.ImageField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)               # Timestamp each post
    modified = models.DateTimeField(auto_now=True)               # Timestamp when each post was modified

class Comment (models.Model):
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)
    text =  models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
