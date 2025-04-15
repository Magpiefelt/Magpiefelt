from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import VideoCategory, VideoContent

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'video_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_type', 'source', 'category', 'is_featured', 'display_order', 'created_at']
    list_filter = ['video_type', 'source', 'category', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'display_order']
    readonly_fields = ['created_at', 'updated_at', 'embed_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'video_type', 'source')
        }),
        ('Embedded Video', {
            'fields': ('embed_code', 'video_url', 'embed_preview'),
            'classes': ('collapse',),
            'description': 'For videos from TikTok, Instagram, or YouTube'
        }),
        ('Local Video', {
            'fields': ('video_file', 'thumbnail'),
            'classes': ('collapse',),
            'description': 'For locally hosted videos'
        }),
        ('Related Content', {
            'fields': ('related_product',),
            'classes': ('collapse',),
            'description': 'Link this video to a product'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'display_order'),
            'description': 'Control how this video appears on the site'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def embed_preview(self, obj):
        if obj.embed_code:
            return format_html(
                '<div style="max-width: 500px; margin-top: 10px;">'
                '<h3>Embed Preview:</h3>'
                '<div style="border: 1px solid #ddd; padding: 10px;">{}</div>'
                '</div>',
                obj.embed_code
            )
        return "No embed code provided."
    embed_preview.short_description = 'Embed Preview'
