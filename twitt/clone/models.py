from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default_profile.png')
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def total_followers(self):
        return self.followers.count()
    
    def total_following(self):
        # Count how many users this user is following
        return Profile.objects.filter(followers=self.user).count()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}\'s post ({self.id})'
    
    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.id}'

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    image = models.ImageField(upload_to='story_images')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user.username}\'s story'
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Stories expire after 24 hours
            self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    image = models.ImageField(upload_to='message_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_message = models.ForeignKey(DirectMessage, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversation')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f'Conversation {self.id}'

