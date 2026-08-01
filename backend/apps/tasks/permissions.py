from common.permissions import IsAdminOrReadOnlyAllowComments


class IsAuthenticatedTaskUser(IsAdminOrReadOnlyAllowComments):
    """Task access: authenticated read/comments, ADMIN-only task management/actions."""

