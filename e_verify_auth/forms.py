# My Django Imports
from django import forms

# My App imports
from e_verify_auth.models import Accounts
from django.contrib.messages.views import SuccessMessageMixin

class AccountCreationForm(forms.ModelForm):
    gender = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    firstname = forms.CharField(required=True, help_text='Please enter your firstname',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    lastname = forms.CharField(required=True,help_text='Please enter your lastname', widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=True, help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True, help_text='Enter a valid phone number', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    password = forms.CharField(required=True, help_text='Password must contain at least 6 characters',
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'Password',
        }
    ))

    picture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))

    gender = forms.ChoiceField(choices=gender, required=False, widget=forms.Select(
        attrs={
            'class':'form-select',
        }
    ))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password too short, should be at least 6 characters!')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Accounts.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already taken!')

        return email

    class Meta:
        model = Accounts
        fields = ('firstname', 'lastname', 'email', 'phone', 'password', 'picture', 'gender')

class OrganizationForm(forms.ModelForm):
    organization = forms.CharField(required=True, help_text='Please Organization name',widget=forms.TextInput(
        attrs={
            'class':'form-control',
        }
    ))

    email = forms.EmailField(required=True, help_text='Enter a valid email address', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'email'
        }
    ))

    phone = forms.CharField(required=True, help_text='Enter a valid phone number', widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'number'
        }
    ))

    password = forms.CharField(required=True, help_text='Password must contain at least 6 characters',
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'type':'Password',
        }
    ))

    picture = forms.ImageField(required=False, help_text='Upload the organization logo', widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'image/png, image/jpeg'
        }
    ))


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password too short, should be at least 6 characters!')

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Accounts.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already taken!')

        return email

    class Meta:
        model = Accounts
        fields = ('organization', 'email', 'phone', 'password', 'picture')
