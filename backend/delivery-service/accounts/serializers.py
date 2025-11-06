from rest_framework import serializers
from .models import User


class SelfUserSerializer(serializers.ModelSerializer):
    """
    Used by any user to view/edit their OWN profile.
    The 'role' field is explicitly read-only, and activation
    status isn't shown (an inactive user can't log in anyway).
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "password"]
        extra_kwargs = {"role": {"read_only": True}, "password": {"write_only": True, "required": False}}

    def update(self, instance, validated_data):
        # Handle password hashing if they're updating it
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class ManagerUserCreateSerializer(serializers.ModelSerializer):
    """
    Used by Managers in the ViewSet 'create' action.
    Allows setting all fields for a new user.
    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "role"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        # Use our custom manager to handle creation
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            role=validated_data["role"],
        )
        return user


class ManagerUserSerializer(serializers.ModelSerializer):
    """
    Used by Managers to LIST, RETRIEVE, and UPDATE *other* users.
    Only 'role' and 'is_active' are editable.
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_active"]
        # Manager can *only* edit role and activate/deactivate
        read_only_fields = ["email", "first_name", "last_name"]
