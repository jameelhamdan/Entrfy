from rest_framework import generics
from django.urls import path
from auth.backend.decorators import view_authenticate
from _common.mixins import APIViewMixin
from _common.helpers import serializer_to_json
from main.models import PostDocument
from main.posts.serializers import ListPostsSerializer, AddPostSerializer, AddPostCommentSerializer, AddPostLikeSerializer


@view_authenticate()
class ListUserPostsView(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        message = 'Successfully Retrieved Posts for {}'.format(user.user_name)
        posts = PostDocument.objects.filter(posted_by=user.uuid).order_by('-created_on')

        posts = serializer_to_json(ListPostsSerializer, posts)

        result = {
            'user_uuid': user.uuid,
            'posts': posts
        }
        return self.get_response(message=message, result=result)


@view_authenticate()
class AddUserPostView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Added Post', result={'post_uuid': result})


@view_authenticate()
class AddUserPostCommentView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddPostCommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        post_uuid, comment_uuid = serializer.validated_data

        result = {
            'post_uuid': post_uuid,
            'comment_uuid': comment_uuid,
        }

        return self.get_response(message='Successfully Added Comment on Post', result=result)


@view_authenticate()
class AddUserPostLikeView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddPostLikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        post_uuid, like_added = serializer.validated_data

        result = {
            'post_uuid': post_uuid,
            'like_added': like_added,
        }

        return self.get_response(message='Successfully Added Like on Post', result=result)


urlpatterns = [
    path('list/', ListUserPostsView.as_view(), name='list_posts'),
    path('add/', AddUserPostView.as_view(), name='add_post'),
    path('comment/', AddUserPostCommentView.as_view(), name='add_post_comment'),
    path('like/', AddUserPostLikeView.as_view(), name='add_post_like'),

]
