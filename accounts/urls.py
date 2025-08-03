from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile & Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.profile_edit, name='profile_edit'),
    path('profile/', views.profile_view, name='profile'),

    # Admin-only routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/all-resumes/', views.view_all_user_resumes, name='view_all_user_resumes'),
    path('admin/users/<int:user_id>/toggle/', views.toggle_staff, name='toggle_staff'),
] 

