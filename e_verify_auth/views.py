# My Django imports
from django.shortcuts import render
from django.views import View
from datetime import date
# My App imports

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