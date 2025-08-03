from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db.models import Q
import logging

from .forms import CustomUserCreationForm, CustomLoginForm, ProfileUpdateForm, UserProfileForm
from .decorators import admin_required
from resumes.models import Resume
from accounts.models import User

logger = logging.getLogger(__name__)


# ✅ Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ✅ Login View
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


# ✅ Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ✅ Dashboard View
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


# ✅ Profile View
@login_required
def profile_view(request):
    form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'user': request.user})


# ✅ Profile Edit View
@login_required
def profile_edit(request):
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    return render(request, 'accounts/profile_edit.html', {'form': form})


# ✅ Admin Dashboard View (superusers or role='admin')
@user_passes_test(lambda u: u.is_authenticated and (u.is_superuser or u.role == 'admin'))
def admin_dashboard(request):
    user_query = request.GET.get('user_query', '')
    resume_query = request.GET.get('resume_query', '')

    users = User.objects.all()
    if user_query:
        users = users.filter(Q(username__icontains=user_query) | Q(email__icontains=user_query))

    resumes = Resume.objects.all()
    if resume_query:
        resumes = resumes.filter(Q(full_name__icontains=resume_query) | Q(email__icontains=resume_query))

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


# ✅ Admin-only: View all resumes
@admin_required
def view_all_user_resumes(request):
    resumes = Resume.objects.all()
    return render(request, 'admin/all_resumes.html', {'resumes': resumes})


# ✅ Superuser only: Toggle staff status
@login_required
def toggle_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        return redirect('admin_dashboard')

    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse('admin_dashboard'))


# ✅ Custom 404 page
def custom_404(request, exception):
    return render(request, '404.html', status=404)


# ✅ Custom 500 page
def custom_500(request):
    return render(request, '500.html', status=500)
