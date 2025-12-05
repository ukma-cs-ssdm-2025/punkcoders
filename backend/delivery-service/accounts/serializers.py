from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import serializers

from .models import User


class SelfUserSerializer(serializers.ModelSerializer):
    """
    Used by any user to view/edit their OWN profile.
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "password"]
        extra_kwargs = {"role": {"read_only": True}, "password": {"write_only": True, "required": False}}

    def validate_password(self, value):
        # for some reason, this is only called for us when using django forms
        validate_password(value, self.instance)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()
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

    def validate(self, attrs):
        # create temp instance to validate against (for the PII similarity check)
        temp_user = User(first_name=attrs.get("first_name"), last_name=attrs.get("last_name"), email=attrs.get("email"))

        password = attrs.get("password")
        try:
            validate_password(password, user=temp_user)
        except DjangoValidationError as exc:
            # so the client knows it's about the password field
            raise serializers.ValidationError({"password": exc.messages})

        return attrs

    def create(self, validated_data):
        try:
            # We pass the raw password here because create_user()
            # in models.py calls set_password() internally.
            user = User.objects.create_user(
                email=validated_data["email"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                password=validated_data["password"],
                role=validated_data["role"],
            )
        except IntegrityError as exc:
            raise serializers.ValidationError({"email": "A user with this email already exists."}) from exc
        return user


class ManagerUserSerializer(serializers.ModelSerializer):
    """
    Used by Managers to LIST and UPDATE existing users.
    Strictly forbids editing Name, Email, or Password.
    Only Role and Active Status can be changed.
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_active"]
        read_only_fields = ["email", "first_name", "last_name"]
