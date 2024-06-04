from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None  # Remove default help text
        self.fields['password2'].help_text = None  # Remove default help text

        # Customize error messages for password fields
        self.fields['password1'].error_messages = {
            'password_mismatch': "The two password fields didn't match.",
        }
        self.fields['password2'].error_messages = {
            'password_mismatch': "The two password fields didn't match.",
        }