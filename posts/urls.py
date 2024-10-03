from django.urls import path, include
from .views import PostListView, PostViewSet, ProfileViewSet, CommentViewSet, CategoryViewSet
from config.yasg import urlpatterns as doc_url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'posts/(?P<post_pk>\d+)/comments', CommentViewSet, basename='comments')
router.register(r'category', CategoryViewSet, basename='categories')
urlpatterns = [
    path('template/', PostListView.as_view(), name='home'),
    path('', include(router.urls)),

]

urlpatterns+= doc_url