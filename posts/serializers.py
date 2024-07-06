from rest_framework import serializers

from posts.models import PostModel, PostLikeModel, CommentModel
from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['uuid', 'avatar', 'username']


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField('get_likes_count')
    comment_count = serializers.SerializerMethodField('get_comments_count')
    user = UserSerializer(read_only=True)
    me_lied = serializers.SerializerMethodField('get_me_liked')

    class Meta:
        model = PostModel
        fields = ['image', 'caption', 'uuid', 'likes_count', 'user', 'me_lied']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_me_liked(self, obj):
        request = self.context.get('request', None)
        return PostLikeModel.objects.filter(post=obj, user=request.user).exists()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    me_lied = serializers.SerializerMethodField('get_me_liked')
    replies = serializers.SerializerMethodField('get_replies')

    class Meta:
        model = CommentModel
        fields = ['id', 'uuid', 'comment', 'created_at', 'me_lied', 'user', 'replies']

    def get_me_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False

    def get_replies(self, obj):
        serializer = self.__class__(obj.child.all(), many=True, context=self.context)
        return serializer.data
