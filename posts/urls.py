from django.urls import path

from posts.views import *

app_name = 'posts'

urlpatterns = [
    # Post Urls
    path('list/', PostListView.as_view(), name='post-list'),
    path('myself/', UserPostListView.as_view(), name='myself'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<int:pk>/like/', PostLikeAPIView.as_view(), name='like'),
    path('<int:pk>/update/', PostUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', PostDeleteAPIView.as_view(), name='post-delete'),


    # Comment Urls
    path('<int:pk>/comments/', PostCommentListView.as_view(), name='post-comments'),
    path('<int:pk>/comments/create/', PostCommentCreateAPIView.as_view(), name='comments-create'),
    path('comment/<int:pk>/like/', PostCommentLikeAPIView.as_view(), name='comment-like'),
    path('<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),

]