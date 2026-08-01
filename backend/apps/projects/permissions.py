from common.permissions import IsAdminOrReadOnly


class IsAuthenticatedProjectUser(IsAdminOrReadOnly):
    """Project access: authenticated read, ADMIN-only management/actions."""

