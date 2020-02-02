from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


class LoggedOutOnlyView(UserPassesTestMixin):
    permission_denied_message = "Page not found."

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can`t go")
        return redirect("core:home")

