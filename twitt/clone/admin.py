from django.contrib import admin
from .models import Profile, Post, Comment, Story, DirectMessage, Conversation

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_followers', 'total_following')
    search_fields = ('user__username', 'user__email')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_likes', 'total_comments')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('created_at',)

class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_expired')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'expires_at')

class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('created_at', 'is_read')

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'updated_at')
    filter_horizontal = ('participants',)
    list_filter = ('updated_at',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(DirectMessage, DirectMessageAdmin)
admin.site.register(Conversation, ConversationAdmin)

