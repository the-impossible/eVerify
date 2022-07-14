# My Django imports
from django.urls import path

# My App imports
from e_verify_auth.views import (
    DashboardView,
    LoginView,
)

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    # AUTHENTICATE
    path('login', LoginView.as_view(), name='login'),
]