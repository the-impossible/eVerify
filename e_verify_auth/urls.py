# My Django imports
from django.urls import path

# My App imports
from e_verify_auth.views import (
    DashboardView,
    LoginView,

    CreateAdminView,
    ManageAdminView,
)

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    # AUTHENTICATE
    path('login', LoginView.as_view(), name='login'),
    # ADMIN
    path('create_admin', CreateAdminView.as_view(), name='create_admin'),
    path('manage_admin', ManageAdminView.as_view(), name='manage_admin'),

]