from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Categories, Comments, Likes, Post, Profile
from .pagination import CommentApiPagination
from .permissions import IsAuthorOrReadOnly
from .serializer import (
    CategoriesSerializer,
    CommentSerializer,
    LikesSerializer,
    PostSerializer,
    ProfileSerializer,
)


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'


class PostApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class BasePermissionViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action in ('create',):
            permission_classes = (IsAuthenticated,)
        elif self.action in ('update', 'partial_update',):
            permission_classes = (IsAuthorOrReadOnly,)
        elif self.action in ('delete',):
            permission_classes = (IsAdminUser, IsAuthorOrReadOnly)
        else:
            permission_classes = (IsAuthenticatedOrReadOnly,)

        return [permission() for permission in permission_classes]


class PostViewSet(BasePermissionViewSet):
    queryset = Post.objects.all().select_related('autor').prefetch_related('categories','comments_post','likes_post')
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['autor', ]
    search_fields = ['title', 'content', 'autor__username']
    ordering_fields = ['updated_at', 'autor', 'likes_post']
    ordering = ['updated_at']

    @action(detail=True, url_path='like', methods=['POST'])
    def like_post(self, request):
        post = self.get_object()
        try:
            like = Likes.objects.get(post=post, user=request.user)
            return Response(data={'msg': 'Like by this user already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Likes.DoesNotExist:
            like = Likes.objects.get_or_create(post=post, user=request.user)
            serializer = LikesSerializer(instance=like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path='unlike', methods=['DELETE'])
    def unlike_post(self, request):
        post = self.get_object()
        try:
            like = Likes.objects.get(post=post, user=request.user)
            like.delete()
            return Response(data={'msg': 'like was delete'})

        except Likes.DoesNotExist:
            return Response(data={'msg': 'This post doesnt like by this user'})


class ProfileViewSet(BasePermissionViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CommentViewSet(BasePermissionViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentApiPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['date_of_edit', 'likes_comment']
    ordering = ['date_of_edit']

    @action(detail=True, url_path='like', methods=['POST'])
    def like_comment(self, request):
        comment = self.get_object()
        try:
            like = Likes.objects.get(comment=comment, user=request.user)
            return Response(data={'msg': 'Like by this user already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Likes.DoesNotExist:
            like = Likes.objects.get_or_create(post=comment, user=request.user)
            serializer = LikesSerializer(instance=like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path='unlike', methods=['DELETE'])
    def unlike_comment(self, request, pk=None):
        post = self.get_object()
        try:
            like = Likes.objects.get(post=post, user=request.user)
            like.delete()
            return Response(data={'msg': 'like was delete'})
        except Likes.DoesNotExist:
            return Response(data={'msg': 'This comment doesnt like by this user'})

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comments.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
