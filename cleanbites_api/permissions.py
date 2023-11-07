from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the object.
        return obj.user == request.user


class IsAccountOwner(permissions.BasePermission):
    """
    permission to allow only owners of an account to edit it.
    """
    def has_permission(self, request, view):
        # check that its an update request and user is modifying his resource only
        if view.kwargs['id']!=request.user.id:
            return False # not grant access
        return True # grant access otherwise