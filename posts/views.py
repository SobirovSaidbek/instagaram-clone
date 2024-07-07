from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostModel, CommentModel, PostLikeModel, CommentLikeModel
from posts.permissions import IsOwner
from posts.serializers import PostSerializer, CommentSerializer
from shared.custom_pagination import CustomPagination, CommentPagination


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.all()


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.filter(user=self.request.user)


class UserLikedPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.filter(id__in=PostLikeModel.objects.filter(user=self.request.user).values_list('post_id', flat=True))

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return CommentModel.objects.filter(post_id=post_id)


class PostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = serializer.data['parent']
        if parent_id:
            serializer.save(parent_id=parent_id)
        post_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, post_id=post_id)


class PostLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post_like = PostLikeModel.objects.filter(post_id=pk, user=self.request.user)
        if post_like.exists():
            post_like.delete()
            response = {
                'status': True,
                'message': 'Successfully unliked'
            }

            return Response(response, status=status.HTTP_200_OK)

        else:
            PostLikeModel.objects.create(post_id=pk, user=self.request.user)
            response = {
                'status': True,
                'message': 'Successfully liked'
            }

            return Response(response, status=status.HTTP_200_OK)


class PostCommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            comment_like = CommentLikeModel.objects.get(comment_id=pk)
            comment_like.delete()
            response = {
                'status': True,
                'message': 'Successfully unliked from comment'
            }
            return Response(response, status=status.HTTP_200_OK)
        except CommentLikeModel.DoesNotExist:
            CommentLikeModel.objects.create(comment_id=pk, user=self.request.user)
            response = {
                'status': True,
                'message': 'Successfully Liked Comment'
            }
            return Response(request, status=status.HTTP_200_OK)


class PostUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def put(self, request, pk):
        post = PostModel.objects.filter(pk=pk)
        if not post.exists():
            response = {
                'status': False,
                'message': 'Post does not exist'
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post.first(), data=request.data, context={'request': request})
        if serializer.is_valid():
            self.check_object_permissions(obj=post.first(), request=request)
            serializer.save()

            response = {
                'status': True,
                'message': 'Successfully Updated'
            }
            return Response(response, status=status.HTTP_200_OK)

        else:

            response = {
                'status': False,
                'message': 'Error updating post',
                'errors': serializer.errors
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CommentSerializer

    def put(self, request, pk):
        comment = CommentModel.objects.filter(pk=pk).first()
        if not comment:
            response = {
                'status': False,
                'message': 'Comment does not exist'
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            self.check_object_permissions(comment, request)
            serializer.save()
            response = {
                'status': True,
                'message': 'Successfully Updated'
            }
            return Response(response, status=status.HTTP_200_OK)

        else:

            response = {
                'status': False,
                'message': 'Error updating post',
                'errors': serializer.errors
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        post = PostModel.objects.filter(pk=pk)
        if not post.first():
            response = {
                'status': False,
                'message': 'Post does not found'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(post.first(), request)
        post.delete()
        response = {
            'status': True,
            'message': 'Successfully deleted'
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        comment = CommentModel.objects.filter(pk=pk)
        if not comment.first():
            response = {
                'status': False,
                'message': 'Comment does not exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(comment, request)
        comment.delete()
        response = {
            'status': True,
            'message': 'Successfully deleted comment'
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
