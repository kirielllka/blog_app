from django.views.generic import ListView
from rest_framework import generics
from .serializer import PostSerializer, ProfileSerializer, CommentSerializer, LikesSerializer
from .models import Post, Profile, Comments, Likes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .permissions import IsAuthorOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .pagination import CommentApiPagination




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
    queryset = Post.objects.all()
    serializer_class = PostSerializer



    @action(detail=True, url_path='like', methods=['POST'])
    def like_post(self, request, pk=None):
        post = self.get_object()
        try:
            like = Likes.objects.get(post=post, user=request.user)
            return Response(data={'msg': 'Like by this user already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Likes.DoesNotExist:
            like = Likes.objects.get_or_create(post=post, user=request.user)
            serializer = LikesSerializer(instance=like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)




class ProfileViewSet(BasePermissionViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CommentViewSet(BasePermissionViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentApiPagination

    @action(detail=True, url_path='like', methods=['POST'])
    def like_comment(self, request, pk=None):
        comment = self.get_object()
        try:
            like = Likes.objects.get(comment=comment, user=request.user)
            return Response(data={'msg': 'Like by this user already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Likes.DoesNotExist:
            like = Likes.objects.get_or_create(post=comment, user=request.user)
            serializer = LikesSerializer(instance=like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comments.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(id = post_id)
        serializer.save(user=self.request.user, post=post)











