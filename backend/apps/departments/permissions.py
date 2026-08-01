from common.permissions import IsAdminOrReadOnly


class IsAuthenticatedDepartmentUser(IsAdminOrReadOnly):
    """Department access: authenticated read, ADMIN-only create/update/delete."""

