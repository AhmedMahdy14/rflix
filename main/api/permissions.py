from rest_framework import permissions
from main.models import *


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsOwnerorAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        return obj.id == user_id or User.objects.get(id=user_id).is_superuser


class IsPartyOwnerorAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        party_owner = None
        if obj.party_memberships.count():
            party_owner = obj.party_memberships.first().id
        return User.objects.get(id=user_id).is_superuser or party_owner == user_id 


class IsMovieRaterOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """

    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        rm_obj = RatingMovie.objects.get(movie=obj, user=request.user)
        return rm_obj.user.id == user_id


