from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend ='allauth.account.auth_backends.AuthenticationBackend'
            messages.success(request, "Registration successful.")
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required
from resumes.models import Resume

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'accounts/dashboard.html', {'resumes': resumes})

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
        return redirect('dashboard')  # or wherever your profile page is
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

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_staff = User.objects.filter(is_staff=True).count()
    total_resumes = Resume.objects.count()
    approved = Resume.objects.filter(moderation_status="approved").count()
    pending = Resume.objects.filter(moderation_status="pending").count()
    rejected = Resume.objects.filter(moderation_status="rejected").count()

    context = {
        'total_users': total_users,
        'total_staff': total_staff,
        'total_resumes': total_resumes,
        'approved': approved,
        'pending': pending,
        'rejected': rejected,
        # Include these if you're using them:
        'resume_form': ResumeSearchForm(),
        'user_form': UserSearchForm(),
        'filtered_users': User.objects.all(),  # or filtered result
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

def toggle_staff(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')

    user = get_user_model().objects.get(id=user_id)
    user.is_staff = not user.is_staff
    user.save()
    return HttpResponseRedirect(reverse('admin_dashboard'))
