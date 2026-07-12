from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*role_names):
    """
    Vérifie que l'utilisateur connecté possède au moins un des rôles indiqués
    (via les tables custom roles/role_user). Les superusers passent toujours.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            from .models import RoleUser
            has_role = RoleUser.objects.filter(
                user=request.user,
                role__role__in=role_names
            ).exists()

            if not has_role:
                messages.error(request, "Vous n'avez pas les droits nécessaires pour accéder à cette page.")
                return redirect('artist_index')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator