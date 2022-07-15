# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# My App imports
from e_verify_auth.models import Accounts
from e_verify_auth.forms import AccountCreationForm

# Create your views here.
class DashboardView(View):
    def get(self, request):
        context = {
            'time':date.today().strftime("%Y-%m-%d"),
        }
        return render(request, 'auth/dashboard.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip().lower()

        if email and password:
            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user}')
                    return redirect('auth:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class CreateAdminView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/create_admin.html'
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:manage_admin")

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        form.instance.is_staff = True
        return super().form_valid(form)

class ManageAdminView(ListView):
    model = Accounts
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=True).order_by('-date_joined')

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logout, to continue login again')

        return redirect('auth:login')