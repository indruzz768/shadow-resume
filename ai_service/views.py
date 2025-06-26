from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from resumes.models import Resume
from ai_service.utils import extract_skills

@login_required
def extract_resume_skills(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    combined_text = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"
    skills = extract_skills(combined_text)

    resume.skills = ", ".join(skills)
    resume.save()

    return redirect('resume_list')  # Or 'dashboard'
