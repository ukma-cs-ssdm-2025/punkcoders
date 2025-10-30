from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    A custom form for creating new users.
    We just need to specify our custom User model.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # Customers don't set their role


class CustomAuthenticationForm(AuthenticationForm):
    """
    A standard login form. We don't need to change much,
    but it's good practice to have it in case you
    want to customize it later.
    """

    pass
