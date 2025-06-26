from django.urls import path
from .api_views import ResumeListCreateAPIView, ResumeDetailAPIView, extract_skills_api

urlpatterns = [
    path('api/', ResumeListCreateAPIView.as_view(), name='api_resume_list_create'),
    path('api/<int:pk>/', ResumeDetailAPIView.as_view(), name='api_resume_detail'),
    path('api/extract-skills/', extract_skills_api, name='api_extract_skills'),  # ✅ Add this
]
# This file defines the URL patterns for the resumes app, mapping URLs to API views.
# It includes paths for listing and creating resumes, retrieving and updating a specific resume, and extracting skills from resumes.

