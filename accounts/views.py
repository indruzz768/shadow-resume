from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib import messages
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.decorators import user_passes_test


logger = logging.getLogger(__name__)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Re-authenticate user to determine the backend properly
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=user.username, password=raw_password)
            login(request, user)  # Now Django knows the backend
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

from django.contrib.auth.decorators import login_required
from resumes.models import Resume

import logging
logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    try:
        resumes = Resume.objects.filter(user=request.user)
        github_skills = request.user.github_skills if hasattr(request.user, 'github_skills') else []
        github_projects = request.user.github_projects if hasattr(request.user, 'github_projects') else []

        return render(request, 'accounts/dashboard.html', {
            'resumes': resumes,
            'github_skills': github_skills,
            'github_projects': github_projects
        })
    except Exception as e:
        logger.error(f"Dashboard view error: {e}")
        raise

from accounts.decorators import admin_required

@admin_required
def view_all_user_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'admin/all_resumes.html', {'resumes': resumes})


@login_required
def profile_edit(request):
    user = request.user
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    return render(request, 'accounts/profile_edit.html', {'form': form})

# accounts/views.py

from .forms import UserProfileForm

@login_required
def profile_view(request):
    user = request.user
    form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form, 'user': user})

# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from accounts.models import User
from resumes.models import Resume
from django.db.models import Q
from .forms import ResumeSearchForm, UserSearchForm


def is_admin_or_superuser(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

@user_passes_test(is_admin_or_superuser)
def admin_dashboard(request):
    user_query = request.GET.get('user_query', '')
    resume_query = request.GET.get('resume_query', '')

    # Filter users
    users = User.objects.all()
    if user_query:
        users = users.filter(
            Q(username__icontains=user_query) |
            Q(email__icontains=user_query)
        )

    # Filter resumes
    resumes = Resume.objects.all()
    if resume_query:
        resumes = resumes.filter(
            Q(full_name__icontains=resume_query) |
            Q(email__icontains=resume_query)
        )

    context = {
        'total_users': User.objects.count(),
        'total_staff': User.objects.filter(is_staff=True).count(),
        'total_resumes': Resume.objects.count(),
        'approved': Resume.objects.filter(moderation_status="approved").count(),
        'pending': Resume.objects.filter(moderation_status="pending").count(),
        'rejected': Resume.objects.filter(moderation_status="rejected").count(),

        'filtered_users': users,
        'filtered_resumes': resumes,
        'user_query': user_query,
        'resume_query': resume_query,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def toggle_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Optional: return 403 if stricter

    # Use get_object_or_404 for better error handling
    user = get_object_or_404(get_user_model(), id=user_id)

    # Prevent user from demoting themselves accidentally
    if user == request.user:
        return redirect('admin_dashboard')

    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse('admin_dashboard'))



def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
