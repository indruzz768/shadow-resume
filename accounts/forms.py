from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
            })
            
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
            'username': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md px-3 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-300 rounded-md px-3 py-2'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md px-3 py-2'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md px-3 py-2'}),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
class ResumeSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search Resumes')

class UserSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search Users')