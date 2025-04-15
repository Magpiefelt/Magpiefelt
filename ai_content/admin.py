from django.contrib import admin
from .models import AIContentType, AIPromptTemplate, AIGeneratedContent

@admin.register(AIContentType)
class AIContentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(AIPromptTemplate)
class AIPromptTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'content_type', 'temperature', 'max_tokens', 'is_active', 'updated_at']
    list_filter = ['content_type', 'is_active']
    search_fields = ['name', 'prompt_text', 'system_message']
    list_editable = ['is_active', 'temperature', 'max_tokens']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'content_type', 'is_active')
        }),
        ('Prompt Configuration', {
            'fields': ('prompt_text', 'system_message'),
            'description': 'Use placeholders like {product_name} in your prompt template.'
        }),
        ('Generation Settings', {
            'fields': ('temperature', 'max_tokens'),
            'description': 'Temperature controls randomness (0.0-1.0). Higher values make output more random.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AIGeneratedContent)
class AIGeneratedContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'get_target_name', 'created_at', 'created_by', 'is_approved']
    list_filter = ['content_type', 'is_approved', 'created_at']
    search_fields = ['prompt_used', 'generated_content']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'prompt_template', 'prompt_used']
    list_editable = ['is_approved']
    
    fieldsets = (
        ('Content Information', {
            'fields': ('content_type', 'prompt_template', 'is_approved')
        }),
        ('Generated Content', {
            'fields': ('generated_content',),
            'description': 'The AI-generated content.'
        }),
        ('Prompt Used', {
            'fields': ('prompt_used',),
            'classes': ('collapse',),
            'description': 'The actual prompt sent to the AI.'
        }),
        ('Related Content', {
            'fields': ('product', 'blog_post', 'social_post'),
            'description': 'The content this was generated for.'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_target_name(self, obj):
        if obj.product:
            return f"Product: {obj.product.title}"
        elif obj.blog_post:
            return f"Blog: {obj.blog_post.title}"
        elif obj.social_post:
            return f"Social: {obj.social_post.title or 'Untitled'}"
        return "No target"
    get_target_name.short_description = 'Target'
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
