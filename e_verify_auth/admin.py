# My Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App imports
from e_verify_auth.models import Accounts

# Register your models here.
class AccountsAdmin(UserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'date_joined', 'last_login', 'is_active', 'is_staff', )
    search_fields = ('email', 'firstname',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Accounts, AccountsAdmin)
