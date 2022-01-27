from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Comment, Group, Post

from .permissions import IsAuthenticatedAndOwner, IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = ()
    queryset = Group.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_queryset(self):
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        queryset = Comment.objects.filter(post_id=self.kwargs['post_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs['post_id'])
        )


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedAndOwner, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        following = get_object_or_404(
            User,
            username=self.request.data['following']
        )
        serializer.save(user=self.request.user, following=following)

    def get_queryset(self):
        queryset = self.request.user.subscribitions.all()
        return queryset
