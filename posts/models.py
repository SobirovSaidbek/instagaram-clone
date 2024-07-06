from django.db import models

from shared.models import BaseModel
from users.models import UserModel


class PostModel(BaseModel):
    image = models.ImageField(upload_to='media/postlar')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.full_name

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class PostLikeModel(BaseModel):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.full_name

    class Meta:
        ordering = ['created_at']
        db_table = 'post_likes'
        verbose_name = 'Post Like'
        verbose_name_plural = 'Posts Likes'


class CommentModel(BaseModel):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_comments')
    comment = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True, blank=True)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'post_comments'
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Posts Comments'


class CommentLikeModel(BaseModel):
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_likes')

    def __str__(self):
        return  self.comment.comment

    class Meta:
        db_table = 'comment_likes'
        verbose_name = 'comment like'
        verbose_name_plural = 'comments likes'