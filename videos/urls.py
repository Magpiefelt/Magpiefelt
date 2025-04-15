from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='video_list'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]
