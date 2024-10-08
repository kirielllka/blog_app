from django.contrib import admin

from .models import Comments, Likes, Post, Profile

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Likes)
