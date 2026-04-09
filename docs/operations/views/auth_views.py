"""Session authentication views for operations web UI."""
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from operations.models import Role


class LoginView(DjangoLoginView):
    template_name = 'operations/auth/login.html'
    redirect_authenticated_user = True


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('operations:login')


class RoleRedirectView(View):
    """After login: send user to role-appropriate home."""

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('operations:login')
        try:
            role = request.user.operations_profile.role
        except Exception:
            return redirect('operations:login')
        if role in (Role.RIDER, Role.DRIVER):
            return redirect('operations:rider_reports')
        if role == Role.PC:
            return redirect('operations:pc_reports')
        if role == Role.ME:
            return redirect('operations:me_reports')
        if role == Role.ADMIN:
            return redirect('operations:me_reports')
        return redirect('operations:rider_reports')
