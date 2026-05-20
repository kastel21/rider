from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from ..models import UserProfile


class LoginView(DjangoLoginView):
    template_name = "operations/auth/login.html"
    redirect_authenticated_user = True


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
