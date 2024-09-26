from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post, Profile, Comments, Likes

class UserSerializer(serializers.ModelSerializer):#для отображения в апи
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PostSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())#скрывает поле
    autor_info = serializers.SerializerMethodField()
    comments_ids = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id','title', 'content','comments_ids','autor','autor_info','like_count','likes', 'created_at', 'updated_at')

    def get_autor_info(self,object):#метод для раскрытия юзера чтобы вместо айди был обьект
        serializer = UserSerializer(object.autor)
        return serializer.data

    def get_comments_ids(self, obj):
        return [comment.id for comment in obj.comments_post.all()]

    def get_likes(self, obj):
        return [like.user.id for like in obj.likes_post.all()]

    def get_like_count(self, obj):
        return len([like.id for like in obj.likes_post.all()])


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())#скрывает поле
    full_name = Profile.full_name
    # user_info = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id','user','full_name','user_patronymic', 'user_birth_date')

    # def get_user_info(self,object):#метод для раскрытия юзера чтобы вместо айди был обьект
    #     serializer = UserSerializer(object.user)
    #     return serializer.data




class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_info = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Comments
        fields = ('id', 'post','post_info', 'user','user_info', 'content','like_count','likes', 'date_of_create', 'date_of_edit')

    def get_user_info(self,object):#метод для раскрытия юзера чтобы вместо айди был обьект
        serializer = UserSerializer(object.user)
        return serializer.data

    def get_post_info(self,object):#метод для раскрытия юзера чтобы вместо айди был обьект
        serializer = PostSerializer(object.post)
        return serializer.data['title']

    def get_likes(self, obj):
        return [like.user.id for like in obj.likes_comment.all()]

    def get_like_count(self, obj):
        return len([like.id for like in obj.likes_comment.all()])



class LikesSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post_info = serializers.SerializerMethodField()

    class Meta:
        model = Likes
        fields = ('id', 'post', 'comment','user', 'user_info', 'post_info', 'likes')

    def get_user_info(self, object):
        serializer = UserSerializer(object.user)
        return serializer.data

    def get_post_info(self, object):
        serializer = PostSerializer(object.post)
        return serializer.data['title']

