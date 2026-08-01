from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
	"""Allow authenticated users to read, but only ADMIN users can change data."""

	message = 'Only admin users can perform this action.'

	def has_permission(self, request, view):
		if not request.user or not request.user.is_authenticated:
			return False
		if request.method in SAFE_METHODS:
			return True
		return getattr(request.user, 'role', None) == 'ADMIN'


class IsAdminOrReadOnlyAllowComments(IsAdminOrReadOnly):
	"""Task permission: comments can be read/added by authenticated users; management is admin-only."""

	def has_permission(self, request, view):
		if not request.user or not request.user.is_authenticated:
			return False
		if getattr(view, 'action', None) == 'comments':
			return True
		return super().has_permission(request, view)

