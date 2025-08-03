from django.urls import path
from . import views
from .api_views import (
    ResumeListCreateAPIView,
    ResumeDetailAPIView,
    ExtractSkillsAPIView,
)

urlpatterns = [
    # Resume CRUD
    path('', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('update/<int:pk>/', views.resume_update, name='resume_update'),
    path('delete/<int:pk>/', views.resume_delete, name='resume_delete'),
    path('view/<int:pk>/', views.resume_detail, name='resume_detail'),

    # File Operations
    path('<int:pk>/delete_file/', views.delete_resume_file, name='delete_resume_file'),
    path('<int:pk>/extract_skills/', views.extract_resume_skills, name='extract_resume_skills'),
    path('<int:resume_id>/download/', views.generate_resume_pdf, name='generate_resume_pdf'),

    # API Endpoints
    path('api/', ResumeListCreateAPIView.as_view(), name='api_resume_list_create'),
    path('api/<int:pk>/', ResumeDetailAPIView.as_view(), name='api_resume_detail'),
    path('api/extract_skills/', ExtractSkillsAPIView.as_view(), name='api_extract_skills'),

    # Moderation
    path('staff/moderation/', views.staff_moderation_view, name='staff_moderation_view'),
    path('staff/moderate/<int:pk>/', views.moderate_resume, name='moderate_resume'),

    # Misc
    path('tailwind-test/', views.tailwind_test_view, name='tailwind_test'),
]

# This file defines the URL patterns for the resumes app, mapping URLs to views.
# It includes paths for listing resumes, creating a new resume, updating an existing resume, and deleting a resume.
