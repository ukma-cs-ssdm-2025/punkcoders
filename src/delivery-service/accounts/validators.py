from django.core.exceptions import ValidationError
from zxcvbn import zxcvbn


class ZxcvbnPasswordValidator:
    """
    A password validator that uses the zxcvbn library to check password strength.
    """

    def __init__(self, min_score=3):
        self.min_score = min_score

    def validate(self, password, user=None):
        """
        Validates the password against the zxcvbn strength estimator.
        """
        # The zxcvbn library returns a score from 0 (terrible) to 4 (excellent).
        # not hardcoding user_inputs because they may change in the future, better to use django's validator
        strength = zxcvbn(password)  # , user_inputs=[user.username if user else None, user.email if user else None])

        if strength["score"] < self.min_score:
            # The feedback from zxcvbn is very user-friendly.
            feedback = strength["feedback"]["warning"] or "This password is too weak."
            suggestions = "\\n".join(strength["feedback"]["suggestions"])
            raise ValidationError(f"{feedback} {suggestions}")

    def get_help_text(self):
        return f"Your password must have a strength score of at least {self.min_score} out of 4."
