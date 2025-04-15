from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class VideoCategory(models.Model):
    """Categories for video content"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Video Categories'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class VideoContent(models.Model):
    """Model for timelapse videos and tutorials"""
    VIDEO_TYPE_CHOICES = (
        ('timelapse', 'Timelapse'),
        ('tutorial', 'Tutorial'),
        ('process', 'Process Video'),
        ('product', 'Product Showcase'),
    )
    
    SOURCE_CHOICES = (
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('local', 'Local Upload'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(VideoCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    description = models.TextField(blank=True)
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPE_CHOICES)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    # For embedded videos
    embed_code = models.TextField(blank=True, help_text="Embed code from TikTok, Instagram, or YouTube")
    video_url = models.URLField(blank=True, help_text="URL to the original video")
    
    # For local videos
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, help_text="MP4 file for locally hosted videos")
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    
    # Product association
    related_product = models.ForeignKey('products.CustomProduct', on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    
    # Display options
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'display_order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('videos:video_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_embedded(self):
        """Check if this is an embedded video"""
        return self.source in ['tiktok', 'instagram', 'youtube'] and bool(self.embed_code)
    
    @property
    def is_local(self):
        """Check if this is a locally hosted video"""
        return self.source == 'local' and bool(self.video_file)
