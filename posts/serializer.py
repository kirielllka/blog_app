
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Profile, Comments, Likes, Categories
class UserSerializer(serializers.ModelSerializer):#для отображения в апи
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id','category_name')



class PostSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())
    autor_info = serializers.SerializerMethodField()
    comments_ids = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    categories = serializers.PrimaryKeyRelatedField(many=True,queryset=Categories.objects.all(), required=False)
    categories_display = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'content',
                  'comments_ids',
                  'categories',
                  'autor','autor_info','like_count','likes', 'created_at', 'updated_at','categories_display')

    def get_autor_info(self,object):#метод для раскрытия юзера чтобы вместо айди был обьект
        serializer = UserSerializer(object.autor)
        return serializer.data

    def get_comments_ids(self, obj):
        return [comment.id for comment in obj.comments_post.all()]

    def get_likes(self, obj):
        return [like.user.id for like in obj.likes_post.all()]

    def get_like_count(self, obj):
        return len([like.id for like in obj.likes_post.all()])

    def get_categories_display(selfself, obj):
        return [{'id':category.id, 'name':category.category_name} for category in obj.categories.all()]

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        post = Post.objects.create(**validated_data)
        post.categories.set(categories_data)
        return post

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])
        instance = super().update(instance, validated_data)
        instance.categories.set(categories_data)
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())#скрывает поле
    full_name = Profile.full_name
    age = Profile.User_age

    class Meta:
        model = Profile
        fields = ('id','user','image','full_name','user_patronymic','age', 'user_birth_date')






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




