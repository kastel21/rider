import json

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ..models import UserProfile
from ..services.remote_jwt import mint_local_rider_tokens, resolve_rider_jwt_tokens


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
            tokens = resolve_rider_jwt_tokens(
                self.request.user,
                api_base,
                form.cleaned_data.get("username", ""),
                form.cleaned_data.get("password", ""),
            )
            if tokens:
                return render(
                    self.request,
                    "operations/auth/login_success.html",
                    {
                        "redirect_url": self.get_success_url(),
                        "ops_jwt_bootstrap_json": json.dumps(tokens),
                        "ops_remote_api_base": api_base,
                        "ops_sync_mode": sync_mode,
                    },
                )
        return response


class RiderJwtBootstrapView(LoginRequiredMixin, View):
    """GET /api/rider/jwt-bootstrap/ — (re)issue JWT for WebView localStorage when sync mode is jwt."""

    def get(self, request):
        sync_mode = getattr(settings, "OPS_SYNC_MODE", "").strip()
        api_base = getattr(settings, "OPS_REMOTE_API_BASE", "").strip()
        if sync_mode != "jwt" or not api_base:
            return JsonResponse({"error": "jwt sync not configured"}, status=404)
        if not _is_rider_like_user(request.user):
            return JsonResponse({"error": "not a rider account"}, status=403)
        tokens = mint_local_rider_tokens(request.user)
        if not tokens:
            return JsonResponse(
                {"error": "could not issue token — complete landing sync and sign in again"},
                status=503,
            )
        return JsonResponse(tokens)


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
