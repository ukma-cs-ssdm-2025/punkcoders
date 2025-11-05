from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import ValidationError, validate_password
from rest_framework.test import APITestCase

User = get_user_model()


class SecurityTests(APITestCase):
    """
    Tests for security-related features of the accounts app,
    such as password hashing.
    """

    def _parse_argon2_params(self, password_hash: str) -> dict:
        """
        A helper method to parse an Argon2 hash string and return a dictionary
        of its effort parameters (m, t, p).
        """
        try:
            # Hash format: argon2$argon2id$v=19$m=65536,t=3,p=4$<salt>$<hash>
            parts = password_hash.split("$")
            if len(parts) < 5 or parts[1] != "argon2id":
                return {}

            param_str = parts[3]
            params = {}
            for part in param_str.split(","):
                key, value = part.split("=")
                params[key] = int(value)
            return params
        except (ValueError, IndexError):
            # Return empty dict if parsing fails for any reason
            return {}

    def test_password_is_hashed_with_argon2id(self):
        """
        Verify that a new user's password is hashed using the Argon2id algorithm
        that the Argon2id hash uses effort values greater than or
        equal to our defined security baseline.
        """
        user = User.objects.create_user(
            username="hash_test_user",
            email="bogus@nunya.com",
            password="a_very_secure_password_123!",
            role=User.Role.MANAGER,
        )

        params = self._parse_argon2_params(user.password)
        self.assertTrue(params, "Password hash is not in Argon2id format.")
        self.assertIn("m", params, "Could not parse memory_cost (m) from hash.")
        self.assertIn("t", params, "Could not parse time_cost (t) from hash.")
        self.assertIn("p", params, "Could not parse parallelism (p) from hash.")
        # OWASP password storage cheat sheet minimums
        self.assertGreaterEqual(params["m"], 12228)  # memory_cost
        self.assertGreaterEqual(params["t"], 3)  # time_cost
        self.assertGreaterEqual(params["p"], 1)  # parallelism

    def test_zxcvbn_works(self):
        """
        Verify that the zxcvbn password validator is functional.
        """
        password_0 = "carpenter"
        password_1 = "defghi6789"
        password_2 = "R0$38uD99"
        password_3 = "asdfghju7654rewq"
        password_4 = "q3p948hgvqp3i4hbnarlmb309q3hi549eirjb"

        with self.assertRaises(ValidationError):
            validate_password(password_0)
        with self.assertRaises(ValidationError):
            validate_password(password_1)
        with self.assertRaises(ValidationError):
            validate_password(password_2)

        # This should not raise an exception
        validate_password(password_3)
        validate_password(password_4)
