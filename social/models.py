from django.db import models
from django.utils.text import slugify

class SocialMediaPlatform(models.Model):
    """Model for different social media platforms"""
    name = models.CharField(max_length=50)
    icon_class = models.CharField(max_length=50, help_text="CSS class for the platform icon")
    
    def __str__(self):
        return self.name

class SocialMediaAccount(models.Model):
    """Model for the store's social media accounts"""
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    profile_url = models.URLField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.platform.name}: {self.username}"

class SocialMediaPost(models.Model):
    """Model for featured social media posts to display on the site"""
    TYPE_CHOICES = (
        ('image', 'Image Post'),
        ('video', 'Video Post'),
        ('carousel', 'Carousel Post'),
    )
    
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post_url = models.URLField(help_text="URL to the original post")
    embed_code = models.TextField(help_text="Embed code provided by the platform")
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='social_media/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_featured', 'display_order', '-created_at']
    
    def __str__(self):
        return f"{self.platform.name} Post: {self.title or self.id}"

class Newsletter(models.Model):
    """Model for newsletter subscribers"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
