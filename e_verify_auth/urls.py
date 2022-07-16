# My Django imports
from django.urls import path

# My App imports
from e_verify_auth.views import (
    DashboardView,

    # AUTHENTICATE
    LoginView,
    LogoutView,
    RegisterView,

    # ADMIN
    CreateAdminView,
    ManageAdminView,
    DeleteUserView,

    # ORG
    CreateOrgView,
    ManageOrgUserView,
)

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    # AUTHENTICATE
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterView.as_view(), name='register'),
    # ADMIN
    path('create_admin', CreateAdminView.as_view(), name='create_admin'),
    path('manage_admin', ManageAdminView.as_view(), name='manage_admin'),
    path('delete_admin/<pk>', DeleteUserView.as_view(), name='delete_admin'),
    # ORG
    path('create_org', CreateOrgView.as_view(), name='create_org'),
    path('manage_org', ManageOrgUserView.as_view(), name='manage_org'),

]