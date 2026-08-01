from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthService:
    """Encapsulates reusable authentication business logic."""

    @staticmethod
    def build_tokens_for_user(user: User) -> dict[str, str]:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        token = RefreshToken(refresh_token)
        if hasattr(token, 'blacklist'):
            token.blacklist()

