from django.shortcuts import redirect
from django.contrib.auth.mixins import (
    UserPassesTestMixin,
    LoginRequiredMixin,
    AccessMixin,
)
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found."

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, _("Can`t go"))
        return redirect("core:home")


class EmailLogInOnlyView(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, _("Can`t go"))
            return redirect("users:login")
        elif not self.request.user.login_method == "email":
            messages.error(self.request, _("Can`t go"))
            return redirect("core:home")
        else:
            return super().dispatch(request, *args, **kwargs)


class LoginInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

