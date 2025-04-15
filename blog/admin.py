from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import BlogCategory, BlogPost

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'is_published', 'ai_content_button']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'ai_content_preview']
    list_editable = ['is_published']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'is_published')
        }),
        ('Content', {
            'fields': ('content', 'featured_image'),
            'description': 'Main content of the blog post'
        }),
        ('AI Content', {
            'fields': ('ai_content_preview',),
            'description': 'AI-generated content for this blog post'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def ai_content_button(self, obj):
        url = reverse('ai_content:generate_blog_post', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Generate Content</a>',
            url
        )
    ai_content_button.short_description = 'AI Content'
    
    def ai_content_preview(self, obj):
        # Get the latest AI content for this blog post
        ai_content = obj.ai_content.order_by('-created_at').first() if hasattr(obj, 'ai_content') else None
        if ai_content:
            approve_url = reverse('ai_content:approve_content', args=[ai_content.id])
            return format_html(
                '<div style="padding: 10px; background-color: #f5f5f5; border-radius: 5px;">'
                '<h3>Generated Content:</h3>'
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
        return "No AI content has been generated yet. Use the 'Generate Content' button in the blog post list."
    ai_content_preview.short_description = 'AI Generated Content'

admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
