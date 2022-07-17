# My Django imports
from django.urls import path

# My App imports
from e_verify_app.views import (
    HomeView,
    ResultView,

)

app_name = 'e_verify'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('result', ResultView.as_view(), name='result'),
]