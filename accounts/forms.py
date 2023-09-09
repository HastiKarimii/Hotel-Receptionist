from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import Receptionist
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm


class ReceptionistCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = Receptionist
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class ReceptionistChangeForm(UserChangeForm):
    class Meta:
        model = Receptionist
        fields = (
            'username',
            'email',
        )


class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Receptionist.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-Mail address."
            self.add_error('email', msg)

        return email
