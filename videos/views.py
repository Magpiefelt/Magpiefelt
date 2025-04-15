from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import VideoCategory, VideoContent

def video_list(request):
    """View for displaying all videos"""
    categories = VideoCategory.objects.all()
    featured_videos = VideoContent.objects.filter(is_featured=True)
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(VideoCategory, slug=category_slug)
        videos = VideoContent.objects.filter(category=category)
        title = f"{category.name} Videos - Magpie Crafts"
    else:
        videos = VideoContent.objects.all()
        title = "All Videos - Magpie Crafts"
    
    # Filter by video type if specified
    video_type = request.GET.get('type')
    if video_type and video_type in dict(VideoContent.VIDEO_TYPE_CHOICES):
        videos = videos.filter(video_type=video_type)
        type_display = dict(VideoContent.VIDEO_TYPE_CHOICES)[video_type]
        title = f"{type_display} Videos - Magpie Crafts"
    
    context = {
        'categories': categories,
        'featured_videos': featured_videos,
        'videos': videos,
        'title': title,
        'video_types': VideoContent.VIDEO_TYPE_CHOICES
    }
    return render(request, 'videos/video_list.html', context)

def video_detail(request, slug):
    """View for displaying a single video"""
    video = get_object_or_404(VideoContent, slug=slug)
    
    # Get related videos (same category or video type)
    related_videos = VideoContent.objects.exclude(id=video.id)
    
    if video.category:
        related_videos = related_videos.filter(category=video.category)[:4]
    else:
        related_videos = related_videos.filter(video_type=video.video_type)[:4]
    
    context = {
        'video': video,
        'related_videos': related_videos,
        'title': f"{video.title} - Magpie Crafts"
    }
    return render(request, 'videos/video_detail.html', context)

def category_detail(request, slug):
    """View for displaying videos filtered by category"""
    category = get_object_or_404(VideoCategory, slug=slug)
    videos = VideoContent.objects.filter(category=category)
    
    context = {
        'category': category,
        'videos': videos,
        'title': f"{category.name} Videos - Magpie Crafts"
    }
    return render(request, 'videos/category_detail.html', context)
