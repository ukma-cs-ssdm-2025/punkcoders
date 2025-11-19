from accounts.models import User
from accounts.serializers import (
    ManagerUserCreateSerializer,
    ManagerUserSerializer,
    SelfUserSerializer,
)
from django.test import TestCase


class UserSerializerTests(TestCase):
    """
    Tests for the User-related serializers.
    These tests run at the serializer level, without the API/view layer.
    """

    def setUp(self):
        """Set up initial users for serializer tests."""
        self.courier_user = User.objects.create_user(
            email="courier@test.com",
            first_name="Courier",
            last_name="User",
            password="password123",
            role=User.Role.COURIER,
        )

    # --- SelfUserSerializer Tests ---

    def test_self_user_serializer_fields(self):
        """Test fields and read-only/write-only properties of SelfUserSerializer."""
        serializer = SelfUserSerializer()
        fields = serializer.get_fields()

        self.assertIn("id", fields)
        self.assertIn("email", fields)
        self.assertIn("first_name", fields)
        self.assertIn("last_name", fields)
        self.assertIn("role", fields)
        self.assertIn("password", fields)

        self.assertTrue(fields["role"].read_only, "Role should be read-only for self-updates.")
        self.assertTrue(fields["password"].write_only, "Password should be write-only.")

    def test_self_user_update_no_password(self):
        """Test updating user details without changing the password."""
        data = {"first_name": "UpdatedFirstName", "last_name": "UpdatedLastName"}
        serializer = SelfUserSerializer(self.courier_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.first_name, "UpdatedFirstName")
        self.assertEqual(instance.last_name, "UpdatedLastName")
        self.assertTrue(instance.check_password("password123"), "Password should not have changed.")

    def test_self_user_update_with_password(self):
        """Test updating user details including the password."""
        data = {"first_name": "NewName", "password": "newpassword456"}
        serializer = SelfUserSerializer(self.courier_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.first_name, "NewName")
        self.assertTrue(instance.check_password("newpassword456"), "Password should be updated.")
        self.assertFalse(instance.check_password("password123"), "Old password should no longer work.")

    def test_self_user_update_role_is_ignored(self):
        """Test that attempting to update 'role' via SelfUserSerializer is ignored."""
        self.assertEqual(self.courier_user.role, User.Role.COURIER)
        data = {"role": User.Role.MANAGER}
        serializer = SelfUserSerializer(self.courier_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        # The role should NOT have changed
        self.assertEqual(instance.role, User.Role.COURIER)
        self.assertNotEqual(instance.role, User.Role.MANAGER)

    # --- ManagerUserCreateSerializer Tests ---

    def test_manager_create_serializer_fields(self):
        """Test fields and properties of ManagerUserCreateSerializer."""
        serializer = ManagerUserCreateSerializer()
        fields = serializer.get_fields()

        self.assertIn("email", fields)
        self.assertIn("first_name", fields)
        self.assertIn("last_name", fields)
        self.assertIn("password", fields)
        self.assertIn("role", fields)
        self.assertTrue(fields["password"].write_only, "Password should be write-only.")

    def test_manager_create_serializer_create_user(self):
        """Test successfully creating a new user with the create serializer."""
        data = {
            "email": "newkitchen@test.com",
            "first_name": "New",
            "last_name": "Kitchen",
            "password": "kitchenpassword",
            "role": User.Role.KITCHEN_STAFF,
        }
        serializer = ManagerUserCreateSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(User.objects.count(), 1)  # Only courier from setUp

        instance = serializer.save()

        self.assertEqual(User.objects.count(), 2)  # Now two users
        self.assertEqual(instance.email, "newkitchen@test.com")
        self.assertEqual(instance.role, User.Role.KITCHEN_STAFF)
        self.assertTrue(instance.check_password("kitchenpassword"))

    def test_manager_create_serializer_missing_fields(self):
        """Test that the create serializer fails if required fields are missing."""
        data = {"email": "incomplete@test.com", "first_name": "Incomplete"}
        serializer = ManagerUserCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("role", serializer.errors)

    # --- ManagerUserSerializer Tests ---

    def test_manager_user_serializer_fields(self):
        """Test fields and read-only properties of ManagerUserSerializer."""
        serializer = ManagerUserSerializer()
        fields = serializer.get_fields()

        read_only = ["email", "first_name", "last_name"]
        editable = ["role", "is_active"]

        for field_name in read_only:
            self.assertTrue(fields[field_name].read_only, f"{field_name} should be read-only.")

        for field_name in editable:
            self.assertFalse(fields[field_name].read_only, f"{field_name} should be editable.")

    def test_manager_user_update_role_and_active(self):
        """Test that a manager can update 'role' and 'is_active'."""
        self.assertTrue(self.courier_user.is_active)
        self.assertEqual(self.courier_user.role, User.Role.COURIER)

        data = {"role": User.Role.KITCHEN_STAFF, "is_active": False}
        serializer = ManagerUserSerializer(self.courier_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertEqual(instance.role, User.Role.KITCHEN_STAFF)
        self.assertFalse(instance.is_active)

    def test_manager_user_update_read_only_fields_ignored(self):
        """Test that read-only fields are ignored during an update."""
        data = {
            "email": "newemail@test.com",
            "first_name": "NewFirstName",
            "role": User.Role.MANAGER,  # This one should change
        }
        serializer = ManagerUserSerializer(self.courier_user, data=data, partial=True)

        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        # Check that read-only fields did NOT change
        self.assertEqual(instance.email, "courier@test.com")
        self.assertEqual(instance.first_name, "Courier")

        # Check that the editable field DID change
        self.assertEqual(instance.role, User.Role.MANAGER)
