from django.urls import include, path
from . import views
from .api_views import ResumeListCreateAPIView, extract_skills_api

urlpatterns = [
    path('', views.resume_list, name='resume_list'),
    path('create/', views.resume_create, name='resume_create'),
    path('update/<int:pk>/', views.resume_update, name='resume_update'),
    path('delete/<int:pk>/', views.resume_delete, name='resume_delete'),
    path('api/', ResumeListCreateAPIView.as_view(), name='api_resume_list_create'),
    path('<int:pk>/delete_file/', views.delete_resume_file, name='delete_resume_file'),
    path('<int:pk>/extract_skills/', views.extract_resume_skills, name='extract_resume_skills'),
    path('download/', views.download_resume, name='download_resume'),
    path('api/extract_skills/', extract_skills_api, name='api_extract_skills'),
    path('<int:resume_id>/download/', views.generate_resume_pdf, name='generate_resume_pdf'),
    path('staff/moderation/', views.staff_moderation_view, name='staff_moderation'),
    path('staff/moderate/<int:pk>/', views.moderate_resume, name='moderate_resume'),
    path('tailwind-test/', views.tailwind_test_view, name='tailwind_test'),
    path('view/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('staff/moderate/<int:pk>/', views.moderate_resume, name='moderate_resume'),
    path('r/<uuid:uuid>/', views.public_resume_view, name='public_resume'),


]
# This file defines the URL patterns for the resumes app, mapping URLs to views.
# It includes paths for listing resumes, creating a new resume, updating an existing resume, and deleting a resume.
