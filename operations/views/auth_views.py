from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from ..models import UserProfile
from ..services.remote_jwt import fetch_remote_rider_tokens


def _is_rider_like_user(user):
    try:
        role = user.profile.role
    except UserProfile.DoesNotExist:
        return False
    return role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER)


class LoginView(DjangoLoginView):
    template_name = "operations/auth/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["ops_remote_api_base"] = getattr(settings, "OPS_REMOTE_API_BASE", "") or ""
        ctx["ops_sync_mode"] = getattr(settings, "OPS_SYNC_MODE", "") or ""
        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        api_base = getattr(settings, "OPS_REMOTE_API_BASE", "").strip()
        sync_mode = getattr(settings, "OPS_SYNC_MODE", "").strip()
        if (
            api_base
            and sync_mode == "jwt"
            and _is_rider_like_user(self.request.user)
        ):
            tokens = fetch_remote_rider_tokens(
                api_base,
                form.cleaned_data.get("username", ""),
                form.cleaned_data.get("password", ""),
            )
            if tokens:
                self.request.session["ops_remote_jwt"] = tokens
        return response


class LogoutView(DjangoLogoutView):
    next_page = None

    def dispatch(self, request, *args, **kwargs):
        self.next_page = reverse("operations:login")
        return super().dispatch(request, *args, **kwargs)


class RoleRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            role = request.user.profile.role
        except UserProfile.DoesNotExist:
            return redirect("operations:rider_reports")

        if role in (UserProfile.Role.PC, UserProfile.Role.ADMIN):
            return redirect("operations:pc_reports")
        if role == UserProfile.Role.ME:
            return redirect("operations:me_metrics")
        return redirect("operations:rider_reports")
