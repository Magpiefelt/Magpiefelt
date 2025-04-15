from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SocialMediaPlatform, SocialMediaAccount, SocialMediaPost, Newsletter

@admin.register(SocialMediaPlatform)
class SocialMediaPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_class']
    search_fields = ['name']

@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'is_active', 'display_order']
    list_filter = ['platform', 'is_active']
    search_fields = ['username']
    list_editable = ['is_active', 'display_order']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('platform', 'username', 'profile_url', 'is_active')
        }),
        ('Display Options', {
            'fields': ('display_order',),
            'description': 'Control the order in which accounts appear on the site'
        }),
    )

@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['title_display', 'platform', 'post_type', 'is_featured', 'created_at', 'ai_content_button']
    list_filter = ['platform', 'post_type', 'is_featured']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    readonly_fields = ['created_at', 'ai_content_preview']
    
    fieldsets = (
        ('Post Information', {
            'fields': ('platform', 'post_type', 'post_url', 'title', 'description')
        }),
        ('Media', {
            'fields': ('embed_code', 'thumbnail'),
            'description': 'Embed code for social media posts or upload a thumbnail'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'display_order'),
            'description': 'Control how this post appears on the site'
        }),
        ('AI Content', {
            'fields': ('ai_content_preview',),
            'description': 'AI-generated content for this social media post'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def title_display(self, obj):
        return obj.title or f"Post {obj.id}"
    title_display.short_description = 'Title'
    
    def ai_content_button(self, obj):
        url = reverse('ai_content:generate_social_content', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Generate Caption</a>',
            url
        )
    ai_content_button.short_description = 'AI Content'
    
    def ai_content_preview(self, obj):
        # Get the latest AI content for this social post
        ai_content = obj.ai_content.order_by('-created_at').first() if hasattr(obj, 'ai_content') else None
        if ai_content:
            approve_url = reverse('ai_content:approve_content', args=[ai_content.id])
            return format_html(
                '<div style="padding: 10px; background-color: #f5f5f5; border-radius: 5px;">'
                '<h3>Generated Caption:</h3>'
                '<div style="margin: 10px 0; padding: 10px; background-color: white; border: 1px solid #ddd;">{}</div>'
                '<div>'
                '<a class="button" href="{}" style="margin-right: 10px;">Approve & Use</a>'
                '<span style="color: #666;">Generated on: {}</span>'
                '</div>'
                '</div>',
                ai_content.generated_content,
                approve_url,
                ai_content.created_at.strftime('%b %d, %Y, %H:%M')
            )
        return "No AI content has been generated yet. Use the 'Generate Caption' button in the social post list."
    ai_content_preview.short_description = 'AI Generated Caption'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'first_name']
    readonly_fields = ['subscribed_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'first_name', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('subscribed_at',),
            'classes': ('collapse',)
        }),
    )
