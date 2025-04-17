from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout
from .models import Profile, Post, Comment, Story, DirectMessage, Conversation
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm, StoryForm, MessageForm

# Add this new custom logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def home(request):
    # Get users that the current user follows
    following_users = User.objects.filter(profile__followers=request.user)
    
    # Get posts from users that the current user follows and the current user's posts
    posts = Post.objects.filter(
        Q(user__in=following_users) | Q(user=request.user)
    ).order_by('-created_at')
    
    # Get active stories from users that the current user follows and the current user's stories
    active_stories = Story.objects.filter(
        Q(user__in=following_users) | Q(user=request.user),
        expires_at__gt=timezone.now()
    ).order_by('-created_at')
    
    context = {
        'posts': posts,
        'active_stories': active_stories,
    }
    return render(request, 'home.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # Check if the current user follows this profile
    is_following = False
    if request.user.is_authenticated:
        is_following = user.profile.followers.filter(id=request.user.id).exists()
    
    context = {
        'user_profile': user,
        'posts': posts,
        'post_count': posts.count(),
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def follow_unfollow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        messages.warning(request, 'You cannot follow yourself.')
        return redirect('profile', username=username)
    
    # Check if already following
    is_following = user_to_follow.profile.followers.filter(id=request.user.id).exists()
    
    if is_following:
        # Unfollow
        user_to_follow.profile.followers.remove(request.user)
        action = 'unfollowed'
        is_now_following = False
    else:
        # Follow
        user_to_follow.profile.followers.add(request.user)
        action = 'followed'
        is_now_following = True
    
    # Get updated counts
    target_followers_count = user_to_follow.profile.followers.count()
    current_user_following_count = Profile.objects.filter(followers=request.user).count()
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_following': is_now_following,
            'target_followers_count': target_followers_count,
            'current_user_following_count': current_user_following_count,
            'message': f'You have {action} {username}.'
        })
    
    messages.success(request, f'You have {action} {username}.')
    return redirect('profile', username=username)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('home')
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post_detail.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        # Unlike
        post.likes.remove(request.user)
        liked = False
    else:
        # Like
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})

@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, 'Your story has been created!')
            return redirect('home')
    else:
        form = StoryForm()
    
    return render(request, 'create_story.html', {'form': form})

@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id, expires_at__gt=timezone.now())
    
    # Get next and previous stories from the same user
    next_story = Story.objects.filter(
        user=story.user, 
        created_at__gt=story.created_at,
        expires_at__gt=timezone.now()
    ).order_by('created_at').first()
    
    prev_story = Story.objects.filter(
        user=story.user, 
        created_at__lt=story.created_at,
        expires_at__gt=timezone.now()
    ).order_by('-created_at').first()
    
    context = {
        'story': story,
        'next_story': next_story,
        'prev_story': prev_story,
    }
    return render(request, 'story_view.html', context)

@login_required
def inbox(request):
    # Get all conversations where the current user is a participant
    conversations = Conversation.objects.filter(participants=request.user)
    
    # Add other_user to each conversation
    for conversation in conversations:
        conversation.other_user = conversation.participants.exclude(id=request.user.id).first()
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'direct_messages.html', context)

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Add other_user to the conversation
    conversation.other_user = conversation.participants.exclude(id=request.user.id).first()
    
    # Get all conversations for the sidebar
    all_conversations = Conversation.objects.filter(participants=request.user)
    for conv in all_conversations:
        conv.other_user = conv.participants.exclude(id=request.user.id).first()
    
    messages_list = DirectMessage.objects.filter(
        Q(sender__in=conversation.participants.all(), receiver=request.user) | 
        Q(sender=request.user, receiver__in=conversation.participants.all())
    ).order_by('created_at')
    
    # Mark messages as read
    unread_messages = messages_list.filter(is_read=False, receiver=request.user)
    for message in unread_messages:
        message.is_read = True
        message.save()
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            
            # Get the other participant
            receiver = conversation.other_user
            message.receiver = receiver
            message.save()
            
            # Update the conversation's last message
            conversation.last_message = message
            conversation.save()
            
            return redirect('conversation', conversation_id=conversation_id)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conversation,
        'conversations': all_conversations,
        'messages_list': messages_list,
        'form': form,
    }
    return render(request, 'conversation.html', context)

@login_required
def new_conversation(request, username):
    receiver = get_object_or_404(User, username=username)
    
    # Check if a conversation already exists between these users
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=receiver
    ).first()
    
    if existing_conversation:
        return redirect('conversation', conversation_id=existing_conversation.id)
    
    # Create a new conversation
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, receiver)
            
            # Create the message
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            
            # Update the conversation's last message
            conversation.last_message = message
            conversation.save()
            
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    context = {
        'receiver': receiver,
        'form': form,
    }
    return render(request, 'new_conversation.html', context)

@login_required
def search(request):
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(caption__icontains=query)
    else:
        users = User.objects.none()
        posts = Post.objects.none()
    
    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search.html', context)

