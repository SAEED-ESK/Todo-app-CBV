# from django.contrib.auth.forms import UserRegisterForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from .forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")
    form_class = UserRegisterForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("todo_list")
        return super().get(*args, **kwargs)

class LoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:todo_list")
