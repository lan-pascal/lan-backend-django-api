from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow user to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must be the `user`.
        return obj == request.user
