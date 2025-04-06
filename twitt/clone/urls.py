from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView



"""urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    # Profile URLs - Note the order is important! Put edit_profile before profile/<str:username>/
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow_unfollow, name='follow_unfollow'),
    
    # Post URLs
    path('post/new/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    
    # Story URLs
    path('story/new/', views.create_story, name='create_story'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),
    
    # Direct Message URLs
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:conversation_id>/', views.conversation, name='conversation'),
    path('inbox/new/<str:username>/', views.new_conversation, name='new_conversation'),
    
    # Search URL
    path('search/', views.search, name='search'),
]

"""

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Fix for logout - use GET method
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Profile URLs - Note the order is important! Put edit_profile before profile/<str:username>/
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow_unfollow, name='follow_unfollow'),
    
    # Post URLs
    path('post/new/', views.create_post, name='create_post'),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('post/<uuid:post_id>/like/', views.like_post, name='like_post'),
    
    # Story URLs
    path('story/new/', views.create_story, name='create_story'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),
    
    # Direct Message URLs
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:conversation_id>/', views.conversation, name='conversation'),
    path('inbox/new/<str:username>/', views.new_conversation, name='new_conversation'),
    
    # Search URL
    path('search/', views.search, name='search'),
]
