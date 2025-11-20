import logging

from accounts.permissions import IsManager
from accounts.services import log_user_out_everywhere
from django.db.models import ProtectedError
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import ManagerUserCreateSerializer, ManagerUserSerializer, SelfUserSerializer

logger = logging.getLogger(__name__)


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

    def perform_update(self, serializer):
        """
        Custom update/partial update logic to handle deactivation.
        """
        instance = serializer.save()
        # log user out the 'is_active' flag was just set to False
        if "is_active" in serializer.validated_data and not instance.is_active:
            log_user_out_everywhere(instance)

    def perform_destroy(self, instance):
        """
        Delete a user if they have no records to their name, deactivate otherwise.
        """
        try:
            instance.delete()
        except ProtectedError:
            log_user_out_everywhere(instance)
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


class LogoutView(APIView):
    """
    An endpoint for a user to logout.
    Takes the 'refresh' token and blacklists it.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as exc:
            # Tell clients exactly why logout failed without masking unexpected server bugs.
            logger.warning("Failed to blacklist refresh token: %s", exc)
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)
