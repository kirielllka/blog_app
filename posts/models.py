from datetime import date

from django.contrib.auth.models import User
from django.db import models



class Post(models.Model):
    title = models.fields.CharField(max_length=250, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Create at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Update at')

    def __str__(self):
        return f'Автор:{self.autor}, Название:{self.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User', related_name='profiles')
    user_patronymic = models.fields.CharField(max_length=150, verbose_name='Patronymic', blank=True, null=True)
    user_birth_date = models.fields.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/images', blank=True, null=True,verbose_name='Image')


    def full_name(self):
        full = []
        user_full_name = self.user.first_name + ' ' + self.user.last_name
        if user_full_name != ' ':
            full.append(user_full_name)
        else:
            full.append(self.user.username)
        if self.user_patronymic:
            full.append(self.user_patronymic)
        return ' '.join(full)

    def User_age(self, obj):
        today = date.today()
        age = today.year - obj.user_birth_date.year
        if today.month < obj.user_birth_date.month or (
                today.month == obj.user_birth_date.month and today.day < obj.user_birth_date.day):
            age -= 1
        return age



    def __str__(self):
        return f'Юзер:{self.user}, Отчество:{self.user_patronymic}'



class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='comment_user')
    content = models.TextField(verbose_name='Text')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='Date of create')#устанавливается при создании
    date_of_edit = models.DateTimeField(auto_now=True, verbose_name='Date of edit')#устанавливается при изменениии только

    def __str__(self):
        return f'Пост{self.post},Автор:{self.user},Дата:{self.date_of_create}'


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='post', related_name='likes_post', blank=True, null=True)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, verbose_name='comment', related_name='likes_comment', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', related_name='likes_user')

    def __str__(self):
        if self.post:
            return f'Пост:{self.post},Пользователь:{self.user}'
        return f'Пользователь:{self.user},Коммент:{self.comment}'

