# My Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# My App imports
from e_verify_app.models import ResultInformation

# Register your models here.
admin.site.register(ResultInformation)
