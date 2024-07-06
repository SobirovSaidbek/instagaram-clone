from django.contrib import admin
from posts.models import *


@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'likes')
    list_filter = ('user', 'caption', 'likes')
    search_fields = ('user', 'user__first_name',)


@admin.register(PostLikeModel)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post',)
    list_filter = ('post',)
    search_fields = ('post',)


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'post')
    list_filter = ('comment',)
    search_fields = ('comment', 'user__first_name',)


@admin.register(CommentLikeModel)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment',)
    list_filter = ('user', 'comment',)
    search_fields = ('comment', 'user__first_name',)