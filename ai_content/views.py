from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import openai
import json
import os

from .models import AIContentType, AIPromptTemplate, AIGeneratedContent
from products.models import CustomProduct
from blog.models import BlogPost
from social.models import SocialMediaPost

def get_openai_client():
    """Initialize and return OpenAI client"""
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return None
    
    return openai.OpenAI(api_key=api_key)

@login_required
def ai_dashboard(request):
    """Dashboard for AI content generation"""
    content_types = AIContentType.objects.all()
    recent_content = AIGeneratedContent.objects.order_by('-created_at')[:10]
    
    context = {
        'content_types': content_types,
        'recent_content': recent_content,
        'title': 'AI Content Dashboard - Magpie Crafts'
    }
    return render(request, 'ai_content/dashboard.html', context)

@login_required
def generate_product_description(request, product_id):
    """Generate AI product description"""
    product = CustomProduct.objects.get(id=product_id)
    
    # Get the appropriate prompt template
    content_type = AIContentType.objects.get(slug='product-description')
    prompt_template = AIPromptTemplate.objects.filter(
        content_type=content_type,
        is_active=True
    ).first()
    
    if not prompt_template:
        messages.error(request, 'No active prompt template found for product descriptions.')
        return redirect('admin:products_customproduct_change', product_id)
    
    # Format the prompt with product details
    prompt = prompt_template.prompt_text.format(
        product_name=product.title,
        product_type=product.get_product_type_display_name(),
        difficulty_level=product.difficulty_level or 'Not specified',
        time_to_complete=product.time_to_complete or 'Not specified',
        materials_included=product.materials_included or 'Not specified',
        techniques_used=product.techniques_used or 'Not specified'
    )
    
    # Call OpenAI API
    client = get_openai_client()
    if not client:
        messages.error(request, 'OpenAI API key not configured.')
        return redirect('admin:products_customproduct_change', product_id)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt_template.system_message or "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=prompt_template.temperature,
            max_tokens=prompt_template.max_tokens
        )
        
        generated_content = response.choices[0].message.content
        
        # Save the generated content
        ai_content = AIGeneratedContent.objects.create(
            content_type=content_type,
            prompt_template=prompt_template,
            prompt_used=prompt,
            generated_content=generated_content,
            product=product,
            created_by=request.user
        )
        
        messages.success(request, 'AI product description generated successfully.')
        
        # If this is an AJAX request, return the content
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'content': generated_content,
                'content_id': ai_content.id
            })
        
        # Otherwise redirect back to the product admin page
        return redirect('admin:products_customproduct_change', product_id)
        
    except Exception as e:
        messages.error(request, f'Error generating content: {str(e)}')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        
        return redirect('admin:products_customproduct_change', product_id)

@login_required
def generate_blog_post(request, blog_id=None):
    """Generate AI blog post content"""
    # Similar implementation to generate_product_description
    # but for blog posts
    pass

@login_required
def generate_social_content(request, post_id=None):
    """Generate AI social media content"""
    # Similar implementation to generate_product_description
    # but for social media posts
    pass

@login_required
def approve_content(request, content_id):
    """Approve AI generated content and apply it to the target"""
    content = AIGeneratedContent.objects.get(id=content_id)
    
    # Apply the content to the appropriate target
    if content.product:
        content.product.description = content.generated_content
        content.product.save()
    elif content.blog_post:
        content.blog_post.content = content.generated_content
        content.blog_post.save()
    elif content.social_post:
        content.social_post.description = content.generated_content
        content.social_post.save()
    
    # Mark as approved
    content.is_approved = True
    content.save()
    
    messages.success(request, 'Content approved and applied successfully.')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    # Redirect to appropriate page based on content type
    if content.product:
        return redirect('admin:products_customproduct_change', content.product.id)
    elif content.blog_post:
        return redirect('admin:blog_blogpost_change', content.blog_post.id)
    elif content.social_post:
        return redirect('admin:social_socialmediapost_change', content.social_post.id)
    
    return redirect('ai_content:dashboard')
