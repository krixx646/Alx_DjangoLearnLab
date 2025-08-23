from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')


    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        if user != self:
            self.followers.add(user)

    def unfollow(self, user):
        """Unfollow another user"""
        if user != self:
            self.followers.remove(user)

    def is_following(self, user):
        """Check if following"""
        return self.followers.filter(id=user.id).exists()
    
    def follower_count(self):
        """Return number of followers"""
        return self.followers.count()
    
    def following_list(self):
        """Return list of users this user is following"""
        return self.following.all()

    def is_followed_by(self, user):
        """Check if user is followed by someone"""
        return user.followers.filter(id=self.id).exists()
    

