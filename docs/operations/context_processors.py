"""Template context processors: expose user role for navbar."""
from operations.models import Role


def operations_nav(request):
    """Add user_role for role-based nav links. Safe when no profile."""
    context = {}
    if request.user.is_authenticated:
        try:
            context['user_role'] = request.user.operations_profile.role
        except Exception:
            context['user_role'] = None
    else:
        context['user_role'] = None
    return context
