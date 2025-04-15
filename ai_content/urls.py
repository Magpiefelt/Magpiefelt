from django.urls import path
from . import views

app_name = 'ai_content'

urlpatterns = [
    path('dashboard/', views.ai_dashboard, name='dashboard'),
    path('generate/product/<int:product_id>/', views.generate_product_description, name='generate_product_description'),
    path('generate/blog/<int:blog_id>/', views.generate_blog_post, name='generate_blog_post'),
    path('generate/social/<int:post_id>/', views.generate_social_content, name='generate_social_content'),
    path('approve/<int:content_id>/', views.approve_content, name='approve_content'),
]
