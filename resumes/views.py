from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Resume
from .forms import ResumeForm
from ai_service.utils import extract_skills, extract_text_from_pdf
from weasyprint import HTML
import os

# ✅ Staff check
def is_staff_user(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser

# ✅ Resume List (user's own)
@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

# ✅ Resume Detail
@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []
    return render(request, 'resumes/resume_detail.html', {
        'resume': resume,
        'skills_list': skills_list,
    })

# ✅ Create Resume (with skill extraction)
@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user

            if resume.resume_file:
                full_path = resume.resume_file.path
                parsed_text = extract_text_from_pdf(full_path)
                resume.summary = parsed_text[:1000]  # Optional summary fill
                text_for_skills = parsed_text
            else:
                text_for_skills = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"

            resume.skills = ", ".join(extract_skills(text_for_skills))
            resume.save()

            return redirect('resume_list')
    else:
        form = ResumeForm()

    return render(request, 'resumes/resume_form.html', {'form': form, 'form_title': 'Create'})

# ✅ Update Resume (with optional file + skill re-extraction)
@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume, user=request.user)
        if form.is_valid():
            resume = form.save(commit=False)

            if 'resume_file' in request.FILES and resume.resume_file:
                full_path = resume.resume_file.path
                parsed_text = extract_text_from_pdf(full_path)
                resume.summary = parsed_text[:1000]
                text_for_skills = parsed_text
            else:
                text_for_skills = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"

            resume.skills = ", ".join(extract_skills(text_for_skills))
            resume.save()
            messages.success(request, 'Resume updated successfully.')
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resumes/resume_form.html', {'form': form, 'form_title': 'Update'})

# ✅ Resume Delete
@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})

# ✅ Manual AI Skill Extraction Trigger
@login_required
def extract_resume_skills(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    text = f"{resume.summary or ''}\n{resume.experience or ''}\n{resume.projects or ''}"
    resume.skills = ", ".join(extract_skills(text))
    resume.save()
    return redirect('dashboard')  # or 'resume_detail'

# ✅ Staff Moderation View
@user_passes_test(is_staff_user)
def staff_moderation_view(request):
    resumes = Resume.objects.filter(moderation_status='pending')
    return render(request, 'resumes/staff_resume_moderation.html', {'resumes': resumes})

# ✅ Staff Resume Moderation (Approve/Reject)
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

# ✅ Resume File Delete (only file, not resume)
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
    return redirect('dashboard')

# ✅ Resume List (API JSON format for frontend JS use)
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

# ✅ PDF Resume Generation
@login_required
def generate_resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    skills_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []
    try:
        html_string = render_to_string("resumes/resume_pdf.html", {"resume": resume, "skills_list": skills_list})
        pdf_file = HTML(string=html_string).write_pdf()
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", status=500)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resume_{resume_id}.pdf"'
    return response

# ✅ Public Resume View
def public_resume_view(request, uuid):
    resume = get_object_or_404(Resume, public_uuid=uuid, moderation_status='approved')
    skill_list = [s.strip() for s in resume.skills.split(',')] if resume.skills else []
    return render(request, 'resumes/public_resume.html', {'resume': resume, 'skills_list': skill_list})

# ✅ Tailwind test view
def tailwind_test_view(request):
    return render(request, 'test_tailwind.html')
