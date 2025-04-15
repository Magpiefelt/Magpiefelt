from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('feed/', views.social_feed, name='social_feed'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
]
