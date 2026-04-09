from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class NotRestoredView(LoginRequiredMixin, TemplateView):
    template_name = "operations/stub_not_restored.html"
