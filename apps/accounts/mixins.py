from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin to strictly enforce that the user has a specific role or roles.
    Allowed roles should be passed as a list of strings in the view.
    Example: allowed_roles = ['admin', 'teacher']
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
            
        role_name = user.role.name.lower()
        
        # Check if the user's role matches any of the allowed roles
        for allowed_role in self.allowed_roles:
            if allowed_role.lower() in role_name:
                return True
                
        # If no match
        raise PermissionDenied("You do not have permission to view this page.")
