from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self",
        related_name="following",
        symmetrical=False,
        blank=True,
        
    )

    def __str__(self):
        return self.username




class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(
        User, 
        related_name="liked_posts",
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}: \n{self.content[:20]}..."