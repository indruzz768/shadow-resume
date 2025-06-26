from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume
from .forms import ResumeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import os
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from ai_service.utils import extract_skills, extract_text_from_pdf
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


def is_staff_user(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

@user_passes_test(is_staff_user)
def staff_moderation_view(request):
    resumes = Resume.objects.filter(moderation_status='pending')
    return render(request, 'resumes/staff_moderation.html', {'resumes': resumes})



@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []
    return render(request, 'resumes/resume_detail.html', {
        'resume': resume,
        'skills_list': skills_list,
    })


@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, user=request.user)
        # If the form is valid, save the resume and extract skills from the uploaded file
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            if resume.resume_file:
                full_path = resume.resume_file.path
                parsed_text = extract_text_from_pdf(full_path)
                resume.summary = parsed_text[:1000]  # Optionally trim
                skills = extract_skills(parsed_text)
                resume.skills = ", ".join(skills)
                resume.save()

            return redirect('resume_list')
    else:
        form = ResumeForm()
    return render(request, 'resumes/resume_form.html', {'form': form, 'form_title': 'Create'})


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume, user=request.user)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            # Re-extract summary and skills if a new file is uploaded
            if 'resume_file' in request.FILES and resume.resume_file:
                full_path = resume.resume_file.path
                parsed_text = extract_text_from_pdf(full_path)
                resume.summary = parsed_text[:1000]  # Optionally trim
                skills = extract_skills(parsed_text)
                resume.skills = ", ".join(skills)
                resume.save()
            messages.success(request, 'Resume updated successfully.')
            return redirect('resume_detail', pk=resume.pk)
        else:
            print("❌ Resume Form Errors:", form.errors)

    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resumes/resume_form.html', {'form': form, 'form_title': 'Update'})


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})

from django.http import JsonResponse

@login_required
def resume_list_api(request):
    resumes = Resume.objects.filter(user=request.user)
    data = [{
        'full_name': r.full_name,
        'headline': r.headline,
        'skills': r.skills.split(", "),
        'created': r.created_at.strftime("%Y-%m-%d"),
    } for r in resumes]
    return JsonResponse({'resumes': data})



@require_POST
@login_required
def delete_resume_file(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if resume.resume_file:
        file_path = resume.resume_file.path
        if os.path.isfile(file_path):
            os.remove(file_path)
        resume.resume_file = None
        resume.save()
    return redirect('dashboard')  # Redirect to a suitable page after deletion

@login_required
def extract_resume_skills(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    
    # Placeholder for AI-based skill extraction
    extracted_skills = "Python, Django, REST API, HTML"

    resume.skills = extracted_skills
    resume.save()
    
    return redirect('dashboard')  # or redirect to resume detail view
# This view is a placeholder for the AI service that extracts skills from resumes.
# In a real application, you would implement the AI logic to extract skills from the resume content.

from django.http import FileResponse

def download_resume(_request):
    # ...logic to generate or locate the file...
    return FileResponse(open('path/to/resume.pdf', 'rb'), as_attachment=True, filename='resume.pdf')



@login_required

def generate_resume_pdf(request, resume_id):
    # Get the resume object
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []

    # Render the resume using a Django template
    try:
        html_string = render_to_string("resumes/resume_pdf.html", {"resume": resume, "skills_list": skills_list})
    except Exception as e:
        return HttpResponse(f"Error rendering PDF template: {e}", status=500)

    # Generate PDF in memory (no temp files, no permission errors)
    pdf_file = HTML(string=html_string).write_pdf()

    # Return as downloadable HTTP response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume_id}.pdf"'
    return response

def is_staff_user(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

@user_passes_test(is_staff_user)
def staff_moderation_view(request):
    resumes = Resume.objects.filter(moderation_status='pending')
    return render(request, 'resumes/staff_resume_moderation.html', {'resumes': resumes})

from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect

@require_POST
@user_passes_test(is_staff_user)
def moderate_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    action = request.POST.get('action')

    if action == 'approve':
        resume.moderation_status = 'approved'
    elif action == 'reject':
        resume.moderation_status = 'rejected'
    
    resume.save()
    return redirect('staff_moderation_view')



def tailwind_test_view(request):
    return render(request, 'test_tailwind.html')

def public_resume_view(request, uuid):
    resume = get_object_or_404(Resume, public_uuid=uuid, moderation_status='approved')
    skill_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []
    return render(request, 'resumes/public_resume.html', {'resume': resume, 'skills_list': skill_list})
