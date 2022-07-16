# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# My App imports
from e_verify_auth.models import Accounts
from e_verify_auth.forms import AccountCreationForm, OrganizationForm, AccountUpdateForm, OrganizationUpdateForm

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

class RegisterView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = OrganizationForm
    template_name = 'auth/register.html'
    success_message = "Account created successfully! You can now login!"

    def get_success_url(self):
        return reverse("auth:login")

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super().form_valid(form)

class CreateOrgView(RegisterView):
    template_name = 'auth/create_org.html'

    def get_success_url(self):
        return reverse("auth:manage_org")

class ManageOrgUserView(ManageAdminView):
    template_name = "auth/manage_org.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=False).order_by('-date_joined')

class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = Accounts
    success_message = "Account deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_admin")

class DeleteOrgView(DeleteUserView):
    def get_success_url(self):
        return reverse("auth:manage_org")

class ProfileView(SuccessMessageMixin, View):
    def get(self, request, pk):
        try:
            user = Accounts.objects.get(pk=pk)
            if user.is_staff:
                context = {
                    'form': AccountUpdateForm(instance=user),
                    'user': user,
                }
            else:
                context = {
                    'form': OrganizationUpdateForm(instance=user),
                    'user': user,
                }
            return render(request, 'auth/profile.html', context)
        except ObjectDoesNotExist:
            messages.error(request, 'User account not found!')
            return redirect('auth:dashboard')

    def post(self, request, pk):
        try:
            user = Accounts.objects.get(pk=pk)
            if 'password' in request.POST:
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if user.is_staff:
                    context = {
                    'form': AccountUpdateForm(instance=user),
                    'user': user,
                }
                else:
                    context = {
                        'form': OrganizationUpdateForm(instance=user),
                        'user': user,
                    }

                if password1 and password2:
                    if password1 != password2:
                        messages.error(request, 'Passwords does not match!')
                        return redirect('auth:profile', pk)

                    if len(password1) < 6 :
                        messages.error(request, 'Password too short, ensure at least 6 characters!')
                        return redirect('auth:profile', pk)

                    user.set_password(password1)
                    user.save()

                    messages.success(request, 'Password reset successful!!')
                    if request.user == user:
                        return redirect('auth:login')

                    if request.user.is_superuser:
                        return redirect('auth:profile', pk)
                    return redirect('auth:login')
            else:
                if user.is_staff:
                    form = AccountUpdateForm(request.POST, request.FILES, instance=user)
                else:
                    form = OrganizationUpdateForm(request.POST, request.FILES, instance=user)

                if form.is_valid() :
                    form.save()
                    messages.success(request, 'Profile updated successfully!')
                    return redirect('auth:profile', pk)

                messages.error(request, 'your response contains invalid data!')
                return render(request, 'auth/profile.html', {'form':form, 'user':user})
        except ObjectDoesNotExist:
            messages.error(request, 'User account not found!')
            return redirect('auth:dashboard')
