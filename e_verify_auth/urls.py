# My Django imports
from django.urls import path

# My App imports
from e_verify_auth.views import (
    DashboardView,
    ProfileView,

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
    DeleteOrgView,

    # RESULT
    UploadResultView,
    ListResultView,
    ManageResultView,
    ResultEditForm,
)

app_name = 'auth'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<pk>', ProfileView.as_view(), name='profile'),
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
    path('delete_org/<pk>', DeleteOrgView.as_view(), name='delete_org'),
    # RESULT
    path('upload_result', UploadResultView.as_view(), name='upload_result'),
    path('manage_result', ManageResultView.as_view(), name='manage_result'),
    path('list_result', ListResultView.as_view(), name='list_result'),
    path('result_form/<pk>', ResultEditForm.as_view(), name='result_form'),
]
