from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import SocialMediaPlatform, SocialMediaAccount, SocialMediaPost, Newsletter
from .forms import NewsletterForm

def social_feed(request):
    """View for displaying social media feed"""
    featured_posts = SocialMediaPost.objects.filter(is_featured=True)
    recent_posts = SocialMediaPost.objects.filter(is_featured=False)[:9]
    social_accounts = SocialMediaAccount.objects.filter(is_active=True)
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'social_accounts': social_accounts,
        'title': 'Social Feed - Magpie Crafts'
    }
    return render(request, 'social/social_feed.html', context)

@require_POST
def newsletter_signup(request):
    """View for handling newsletter signups"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')
            
            # Check if email already exists
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'This email is already subscribed to our newsletter.'
                })
            
            # Create new subscriber
            Newsletter.objects.create(
                email=email,
                first_name=first_name
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please enter a valid email address.'
            })
    
    # Handle non-AJAX requests
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        first_name = form.cleaned_data.get('first_name', '')
        
        # Check if email already exists
        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, 'This email is already subscribed to our newsletter.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        # Create new subscriber
        Newsletter.objects.create(
            email=email,
            first_name=first_name
        )
        
        messages.success(request, 'Thank you for subscribing to our newsletter!')
    else:
        messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))
