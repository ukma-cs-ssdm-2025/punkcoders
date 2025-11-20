from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    """
    Allows access only to users with the 'Manager' role.
    """

    def has_permission(self, request, view):
        # We check that the user is authenticated (logged in)
        # AND that their role is 'MANAGER'.
        return bool(request.user and request.user.is_authenticated and request.user.role == "MANAGER")


class IsCourier(BasePermission):
    """
    Allows access only to users with the 'Courier' role.
    """

    def has_permission(self, request, view):
        # We check that the user is authenticated (logged in)
        # AND that their role is 'COURIER'.
        return bool(request.user and request.user.is_authenticated and request.user.role == "COURIER")


class IsKitchenStaff(BasePermission):
    """
    Allows access only to users with the 'Kitchen Staff' role.
    """

    def has_permission(self, request, view):
        # We check that the user is authenticated (logged in)
        # AND that their role is 'KITCHEN_STAFF'.
        return bool(request.user and request.user.is_authenticated and request.user.role == "KITCHEN_STAFF")
