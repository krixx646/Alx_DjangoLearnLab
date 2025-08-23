from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
# Create your models here.

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='Author', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
    

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Ensure a user can like a post only once

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'
    
class Emoji(models.Model):
    name = models.CharField(max_length=50)  # e.g., "smile", "heart", "thumbs_up"
    unicode = models.CharField(max_length=10)  # e.g., "😊", "❤️", "👍"
    post = models.ForeignKey('Post', related_name='emojis', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emojis', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'name')  # one emoji per user per post

    def __str__(self):
        return f"{self.user.username} reacted with {self.name} to {self.post.title}"
    


class followers(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed_user')  # Ensure a user can follow another user only once

    def __str__(self):
        return f'{self.user.username} follows {self.followed_user.username}'