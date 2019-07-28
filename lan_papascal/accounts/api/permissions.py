from rest_framework import permissions

class IsUserOrReadOnlyIfPublic(permissions.BasePermission):
    """
    Object-level permission to only allow user to edit it.
    Assumes the model is the user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        isObjUser = obj == request.user

        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or isObjUser
        else:
            # Instance must be the `user`.
            return isObjUser
