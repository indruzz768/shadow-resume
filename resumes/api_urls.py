from django.urls import path
from .api_views import ResumeListCreateAPIView, ResumeDetailAPIView, ExtractSkillsAPIView

urlpatterns = [
    path('api/', ResumeListCreateAPIView.as_view(), name='api_resume_list_create'),
    path('api/<int:pk>/', ResumeDetailAPIView.as_view(), name='api_resume_detail'),
    path('api/extract-skills/', ExtractSkillsAPIView.as_view(), name='api_extract_skills'),
]
