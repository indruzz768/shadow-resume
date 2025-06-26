from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_photo']  # Add more fields if needed
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_photo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        
class ResumeSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search Resumes')

class UserSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search Users')