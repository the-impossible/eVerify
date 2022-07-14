# My Django imports
from django.shortcuts import render
from django.views import View

# My App imports

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request, 'auth/dashboard.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')