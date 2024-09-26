from django.urls import path, include
from .views import PostListView, PostViewSet, ProfileViewSet, CommentViewSet
# from .views import PostListView, PostApiView, PostList,PostDetailed
from config.yasg import urlpatterns as doc_url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'posts/(?P<post_pk>\d+)/comments', CommentViewSet, basename='comments')
urlpatterns = [
    path('template/', PostListView.as_view(), name='home'),
    # path('posts/', PostList.as_view(), name='apiv1'),
    # path('posts/<int:pk>', PostDetailed.as_view(), name='detail')
    path('', include(router.urls)),
    # path('posts/<int:post_pk>/comments/', CommentsListApiViewPost.as_view(), name='comment-post')

]

urlpatterns+= doc_url