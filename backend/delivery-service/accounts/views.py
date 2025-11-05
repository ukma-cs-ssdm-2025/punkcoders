from rest_framework import viewsets, generics, permissions
from django.db.models import ProtectedError
from .models import User
from .serializers import SelfUserSerializer, ManagerUserSerializer, ManagerUserCreateSerializer
from accounts.permissions import IsManager


class UserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Managers to perform CRUD on *other* users.
    """

    # Use the Manager serializer by default
    serializer_class = ManagerUserSerializer
    permission_classes = [IsManager]

    def get_queryset(self):
        """
        Ovverides queryset to exclude self.
        This prevents a manager from changing their own role or deleting
        themselves from this endpoint.
        """
        return User.objects.all().exclude(pk=self.request.user.pk)

    def get_serializer_class(self):
        """
        Dynamically choose the serializer based on the action.
        - 'create' -> Use the one that requires all fields
        - 'list', 'update', etc. -> Use the one that only allows 'role' edits
        """
        if self.action == "create":
            return ManagerUserCreateSerializer
        return ManagerUserSerializer

    def perform_destroy(self, instance):
        """
        Delete a user if they have no records to their name, deactivate otherwise.
        """
        try:
            instance.delete()
        except ProtectedError:
            instance.is_active = False
            instance.save()


class SelfUserView(generics.RetrieveUpdateAPIView):
    """
    An endpoint for any user to view and edit their own profile.
    """

    serializer_class = SelfUserSerializer
    # Any logged-in user can access this
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        The object is always just the user making the request.
        """
        return self.request.user
