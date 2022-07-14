# My Django imports
from django.shortcuts import render
from django.views import View
from datetime import date
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

class CreateAdminView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/create_admin.html'
    success_message = "Account created successfully!"
    success_url = 'dashboard'

    # def get_success_url(self):
    #     return reverse("users:profile", kwargs={
    #         'pk':self.request.user.userprofile.profile_id
    #     })

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        # form.instance.password = set_password(form.instance.password)
        return super().form_valid(form)

class ManageAdminView(ListView):
    model = Accounts
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=True).order_by('-date_joined')