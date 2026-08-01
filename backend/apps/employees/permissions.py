from common.permissions import IsAdminOrReadOnly


class IsAuthenticatedEmployeeUser(IsAdminOrReadOnly):
    """Employee access: authenticated read, ADMIN-only create/update/delete."""

