from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken


def log_user_out_everywhere(instance):
    tokens = OutstandingToken.objects.filter(user=instance)
    for token in tokens:
        try:
            RefreshToken(token.token).blacklist()
        except TokenError:
            pass  # token's already invalid, no worries
