from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def voyant_required(view_func):
    """Réservé aux voyants."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_voyant() and not request.user.is_superuser:
            messages.error(request, "Accès réservé aux voyants.")
            return redirect('carnet:liste_fiches')
        return view_func(request, *args, **kwargs)
    return wrapper


def responsable_required(view_func):
    """Réservé aux responsables et admins."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_responsable() or request.user.is_admin_role()):
            messages.error(request, "Accès réservé aux responsables.")
            return redirect('carnet:liste_fiches')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Réservé aux admins uniquement."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.is_admin_role():
            messages.error(request, "Accès réservé aux administrateurs.")
            return redirect('carnet:liste_fiches')
        return view_func(request, *args, **kwargs)
    return wrapper