from posts.models import Comments
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj,Comments):
            return obj.user == request.user
        return obj.autor == request.user
