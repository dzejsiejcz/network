from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }




class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked")
    like_date = models.DateTimeField('date liked', auto_now_add=True)

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    follow_date = models.DateTimeField('date added', auto_now_add=True)

    class Meta:
        verbose_name = "friend"
        verbose_name_plural = "friends"
