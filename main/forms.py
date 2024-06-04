from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, AccountSettings
from django.contrib.auth.forms import PasswordChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
                # Set custom labels
        self.fields['username'].label = "User Name:"
        self.fields['email'].label = "Email Address:"
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Confirm Password:"


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
        
        
        
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  
    
class ProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['profile_picture']
        labels = {
            'profile_picture': ''  # Exclude automatic label rendering
        }
        required_css_class = ''  # Remove the asterisk from required fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            if user.profile.profile_picture:
                self.fields['profile_picture'].initial = user.profile.profile_picture.url
        self.fields['profile_picture'].widget.attrs['class'] = 'form-control-file custom-file-input'
        self.fields['profile_picture'].widget.attrs['accept'] = 'image/*'
        self.fields['profile_picture'].widget.attrs['style'] = 'display: none;'  # Hide the current profile picture
        
        
class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = AccountSettings
        fields = ['receive_newsletter', 'two_factor_auth']  # Adjust fields as per your AccountSettings model

    def __init__(self, *args, **kwargs):
        super(AccountSettingsForm, self).__init__(*args, **kwargs)
        self.fields['receive_newsletter'].label = "Receive Newsletter"
        self.fields['two_factor_auth'].label = "Two-Factor Authentication"

# The PasswordChangeForm is provided by Django and doesn't need to be redefined


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set custom labels
        self.fields['old_password'].label = 'Old Password'
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password2'].label = 'New Password Confirmation'

        # Remove help text for password fields
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = None

        # Set autofocus attribute to False for old password field
        self.fields['old_password'].widget.attrs['autofocus'] = False