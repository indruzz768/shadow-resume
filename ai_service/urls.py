from django.urls import path
from . import views

urlpatterns = [
    path('extract/<int:resume_id>/', views.extract_resume_skills, name='extract_resume_skills'),
]
# This file defines the URL patterns for the AI service, specifically for extracting skills from resumes.
# It includes a path for extracting skills from a resume based on its ID.