from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to users with the 'Manager' role.
    """

    def has_permission(self, request, view):
        # We check that the user is authenticated (logged in)
        # AND that their role is 'MANAGER'.
        return bool(request.user and request.user.is_authenticated and request.user.role == "MANAGER")
