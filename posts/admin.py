from django.contrib import admin
from .models import Post, Profile, Comments, Likes

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comments)
admin.site.register(Likes)
