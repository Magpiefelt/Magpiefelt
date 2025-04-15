from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class AIContentType(models.Model):
    """Model for different types of AI-generated content"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class AIPromptTemplate(models.Model):
    """Model for storing prompt templates for AI content generation"""
    name = models.CharField(max_length=200)
    content_type = models.ForeignKey(AIContentType, on_delete=models.CASCADE, related_name='prompt_templates')
    prompt_text = models.TextField(help_text="Template text with placeholders like {product_name}, {materials}, etc.")
    system_message = models.TextField(blank=True, help_text="Optional system message to guide AI behavior")
    temperature = models.FloatField(default=0.7, help_text="Controls randomness (0.0-1.0)")
    max_tokens = models.IntegerField(default=500, help_text="Maximum length of generated content")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.content_type.name})"

class AIGeneratedContent(models.Model):
    """Model for storing AI-generated content"""
    content_type = models.ForeignKey(AIContentType, on_delete=models.CASCADE, related_name='generated_content')
    prompt_template = models.ForeignKey(AIPromptTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    prompt_used = models.TextField(help_text="The actual prompt sent to the AI")
    generated_content = models.TextField()
    
    # Optional relations to other models
    product = models.ForeignKey('products.CustomProduct', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_content')
    blog_post = models.ForeignKey('blog.BlogPost', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_content')
    social_post = models.ForeignKey('social.SocialMediaPost', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_content')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Whether this content has been approved for use")
    
    def __str__(self):
        return f"{self.content_type.name} for {self.product or self.blog_post or self.social_post or 'Unknown'}"
    
    class Meta:
        ordering = ['-created_at']
