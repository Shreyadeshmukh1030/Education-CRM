from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin to strictly enforce that the user has a specific role or roles.
    Allowed roles should be passed as a list of strings in the view.
    Example: allowed_roles = ['Admin', 'Teacher']
    """
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
            
        # Superusers can always access
        if user.is_superuser:
            return True
            
        if not getattr(user, 'role', None):
            return False
            
        role_name = user.role.name
        
        # Check if the user's exact role name matches any of the allowed roles
        if role_name in self.allowed_roles:
            return True
                
        # If no match
        raise PermissionDenied("You do not have permission to view this page.")

class SchoolIsolationMixin:
    """
    Ensures that any queryset is isolated to the user's school.
    Must be used with views that have a `get_queryset` method.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        
        # Assuming the model has a 'school' field
        if hasattr(qs.model, 'school'):
            return qs.filter(school=self.request.user.school)
            
        return qs
