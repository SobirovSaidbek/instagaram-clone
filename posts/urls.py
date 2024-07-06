from django.urls import path

from posts.views import *

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('create/', PostCreateAPIView.as_view(), name='create'),
    path('<int:pk>/comments/', PostCommentListView.as_view(), name='post-comments'),
    path('<int:pk>/comments/create/', PostCommentCreateAPIView.as_view(), name='comments-create'),

    # Like Urls
    path('<int:pk>/like/', PostLikeAPIView.as_view(), name='like'),
    path('comment/<int:pk>/like/', PostCommentLikeAPIView.as_view(), name='comment-like'),

    # Post Update Urls
    path('update/<int:pk>/', PostUpdateAPIView.as_view(), name='update')
]