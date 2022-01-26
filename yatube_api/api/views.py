from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Comment, Follow, Group, Post

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
    queryset = Comment.objects.all()

    def get_queryset(self):
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        queryset = Comment.objects.filter(post_id=self.kwargs['post_id'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, pk=self.kwargs['post_id'])
        )
        return super().perform_create(serializer)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedAndOwner, )
    queryset = Follow.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        if self.request.data['following'] == self.request.user.username:
            raise ValidationError("You can't subscribe to yourself!")
        try:
            following = get_object_or_404(
                User,
                username=self.request.data['following']
            )
            serializer.save(user=self.request.user, following=following)
        except IntegrityError:
            raise ValidationError('You already subscribed!')

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset
