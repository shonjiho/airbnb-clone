import os
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, reverse
from . import forms
from . import models

import requests


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {
        "email": "jihoson94@gmail.com"
    }

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "email": "jihoson94@gmail.com",
        "first_name": "jiho",
        "last_name": "son",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(self, key: str):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # todo: add success message
    except models.User.DoesNotExist:
        # todo error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user')


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        if code is not None:
            result = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"}
            )
            result_json = result.json()
            error = result_json.get('error', None)
            if error is not None:
                raise GithubException()
            else:
                access_token = result_json.get('access_token', None)
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json"
                    }
                )
                profile = profile_request.json()
                username = profile.get('login', None)
                if username is not None:
                    email = profile.get('email')
                    name = profile.get('name')
                    bio = profile.get('bio')
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            username=email,
                            first_name=name,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB)
                        user.set_unusable_password()
                        user.save()

                    login(request, user)
                    return redirect(reverse("core:home"))

                else:
                    raise GithubException()
        raise GithubException()

    except GithubException:
        return redirect(reverse("users:login"))
