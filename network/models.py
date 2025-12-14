from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):  
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} posted {self.content} on {self.timestamp.strftime('%d %b %y %H:%M:%S')}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followung")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followedby")

    def __str__(self):
        return f"{self.user} is following {self.user_follower}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"