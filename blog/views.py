from django.shortcuts import render, get_object_or_404
from .models import BlogCategory, BlogPost

def blog_list(request):
    """View for displaying all published blog posts"""
    posts = BlogPost.objects.filter(is_published=True)
    categories = BlogCategory.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'title': 'Felting Tips & Tutorials'
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """View for displaying a single blog post"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    context = {
        'post': post,
        'title': post.title
    }
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, category_slug):
    """View for displaying blog posts filtered by category"""
    category = get_object_or_404(BlogCategory, slug=category_slug)
    posts = BlogPost.objects.filter(category=category, is_published=True)
    
    context = {
        'category': category,
        'posts': posts,
        'title': f'{category.name} - Felting Tips & Tutorials'
    }
    return render(request, 'blog/blog_category.html', context)
