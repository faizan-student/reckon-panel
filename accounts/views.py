from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import CustomUser


class UserRegisterView(CreateView):
    model = CustomUser
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    # Only these fields at registration time
    fields = ["email", "employee_id", "full_name", "phone_number", "password"]

    def form_valid(self, form):
        form.instance.username = form.cleaned_data["email"]  # Required by AbstractUser
        form.instance.password = make_password(
            form.cleaned_data["password"]
        )  # Hash password
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())  # Important: log the user in
        return redirect("root-page")  # Redirect after successful login


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("profile_update")

    fields = [
        "department",
        "designation",
        "employment_type",
        "access_level",
        "supervisor",
        "date_of_joining",
        "profile_picture",
    ]

    def get_object(self):
        return self.request.user  # Update the logged-in user only


class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("login")
