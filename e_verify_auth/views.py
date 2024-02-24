# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# My App imports
from e_verify_auth.models import Accounts
from e_verify_app.models import ResultInformation
from e_verify_auth.forms import AccountCreationForm, OrganizationForm, AccountUpdateForm, OrganizationUpdateForm, ResultForm, EditResultForm

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request):
        context = {
            'time':date.today().strftime("%Y-%m-%d"),
            'admin':Accounts.objects.all().count(),
            'clients':Accounts.objects.filter(is_staff=False).count(),
            'cert': ResultInformation.objects.all().count(),
        }
        return render(request, 'auth/dashboard.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip()


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

class CreateAdminView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'auth:login'
    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/create_admin.html'
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:manage_admin")

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        form.instance.email = form.instance.email.strip().lower()
        form.instance.is_staff = True
        return super().form_valid(form)

class ManageAdminView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    model = Accounts
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=True).order_by('-date_joined')

class LogoutView(LoginRequiredMixin, View):
    login_url = 'auth:login'
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
        form.instance.email = form.instance.email.strip().lower()
        return super().form_valid(form)

class CreateOrgView(LoginRequiredMixin, RegisterView):
    login_url = 'auth:login'
    template_name = 'auth/create_org.html'

    def get_success_url(self):
        return reverse("auth:manage_org")

class ManageOrgUserView(ManageAdminView):
    login_url = 'auth:login'
    template_name = "auth/manage_org.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=False).order_by('-date_joined')

class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'auth:login'
    model = Accounts
    success_message = "Account deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_admin")

class DeleteOrgView(DeleteUserView):
    login_url = 'auth:login'
    def get_success_url(self):
        return reverse("auth:manage_org")

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, View):
    login_url = 'auth:login'
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

class UploadResultView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'auth:login'
    model = ResultInformation
    form_class = ResultForm
    template_name = 'auth/upload_result.html'
    success_message = "Result Information uploaded!"

    def get_success_url(self):
        return reverse("auth:manage_result")

class ManageResultView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request):
        return render(request, 'auth/manage_result.html')

class ListResultView(ManageAdminView):
    login_url = 'auth"login' 
    template_name = "partials/result_list.html"

    def get_queryset(self):
        return ResultInformation.objects.all().order_by('-date')

class ResultEditForm(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request, pk):
        result = ResultInformation.objects.get(pk=pk)
        form = EditResultForm(instance=result)
        return render(request, 'auth/result_form.html', {'form':form, 'result':result})

    def post(self, request, pk):
        result = ResultInformation.objects.get(pk=pk)
        form = EditResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result has been updated!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        messages.error(request, f'{form.errors.as_text()}')
        return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

class DeleteResultView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'auth:login'
    model = ResultInformation
    success_message = "Result deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_result")

class VerifyResult(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request):
        return render(request, 'auth/verify_result.html')

    def post(self, request):
        qs =  request.POST.get('search')
        result = ResultInformation.objects.filter(cert_no=qs)

        if result:
            return render(request, 'partials/result_content.html', context={'result':result[0], 'qs':qs})
        else:
            messages.error(request, 'Result not found! try inputting a valid cert_no')
        return render(request, 'partials/result_empty.html', {'qs':qs})

class SearchResult(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def post(self, request):
        qs =  request.POST.get('qs')
        result = ResultInformation.objects.filter(cert_no=qs)
        if result:
            return render(request, 'auth/verify_result.html', context={'result':result[0], 'qs':qs})
        else:
            messages.error(request, 'Result not found! try inputting a valid cert_no')
        return render(request, 'auth/verify_result.html', {'qs':qs})
