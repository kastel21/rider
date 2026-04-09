"""PC referred samples list and capture."""

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from operations.forms import ReferredSampleForm
from operations.permissions import OperationsLoginRequiredMixin, PCRequiredMixin
from operations.selectors import get_referred_samples_queryset


class ReferredSamplesModuleView(OperationsLoginRequiredMixin, PCRequiredMixin, View):
    template_name = "operations/pc/referred_samples.html"

    def get(self, request):
        qs = get_referred_samples_queryset(request.user)
        form = ReferredSampleForm(user=request.user)
        return render(request, self.template_name, {"object_list": qs, "form": form})

    def post(self, request):
        qs = get_referred_samples_queryset(request.user)
        form = ReferredSampleForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Record saved.")
            return redirect(reverse("operations:pc_referred_samples_list"))
        return render(request, self.template_name, {"object_list": qs, "form": form})
