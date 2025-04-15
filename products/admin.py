from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import CustomProduct

class CustomProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_type', 'price_display', 'difficulty_level', 'is_public', 'ai_content_button']
    list_filter = ['product_type', 'is_public', 'difficulty_level']
    search_fields = ['title', 'description', 'materials_included', 'techniques_used']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['ai_content_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'product_type', 'is_public')
        }),
        ('Pricing', {
            'fields': ('price',),
        }),
        ('Product Details', {
            'fields': ('difficulty_level', 'time_to_complete', 'materials_included', 'techniques_used'),
            'classes': ('collapse',),
            'description': 'Additional details specific to felting products'
        }),
        ('AI Content', {
            'fields': ('ai_content_preview',),
            'description': 'AI-generated content for this product'
        }),
    )
    
    def price_display(self, obj):
        return f"${obj.price.incl_tax}" if obj.price else "-"
    price_display.short_description = 'Price'
    
    def ai_content_button(self, obj):
        url = reverse('ai_content:generate_product_description', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Generate Description</a>',
            url
        )
    ai_content_button.short_description = 'AI Content'
    
    def ai_content_preview(self, obj):
        # Get the latest AI content for this product
        ai_content = obj.ai_content.order_by('-created_at').first()
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
        return "No AI content has been generated yet. Use the 'Generate Description' button in the product list."
    ai_content_preview.short_description = 'AI Generated Content'

admin.site.register(CustomProduct, CustomProductAdmin)
