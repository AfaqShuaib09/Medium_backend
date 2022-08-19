''' Custom Permissions for the blog_posts Api'''
from rest_framework import permissions


class PostOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to make changes to it. (PUT, PATCH, DELETE)
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user has the permission.
        """
        return obj.posted_by == request.user or request.method in permissions.SAFE_METHODS

class CommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to make changes to it. (PUT, PATCH, DELETE)
    """

    def has_object_permission(self, request, view, obj):
        """ Checks if the user has the permission."""
        return obj.owner == request.user or request.method in permissions.SAFE_METHODS

class ReportOwnerOrReadOnly(permissions.BasePermission):
    """ Custom permission to only allow owners of an object to make changes to it. (PUT, PATCH, DELETE) """

    def has_object_permission(self, request, view, obj):
        """ Checks if the user has the permission."""
        return obj.reported_by == request.user or request.method in permissions.SAFE_METHODS
