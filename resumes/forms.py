from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'phone', 'headline', 'summary', 'skills', 'education', 'experience', 'projects', 'certifications', 'resume_file', 'status', 'moderation_status', 'address', 'email']
        widgets = {
            'skills': forms.Textarea(attrs={'placeholder': 'Enter skills separated by commas'}),
            'education': forms.Textarea(attrs={'placeholder': 'Enter education details'}),
            'experience': forms.Textarea(attrs={'placeholder': 'Enter work experience'}),
            'projects': forms.Textarea(attrs={'placeholder': 'Enter project details'}),
            'certifications': forms.Textarea(attrs={'placeholder': 'Enter certifications'}),
        }
        labels = {
            'full_name': 'Full Name',
            'headline': 'Headline',
            'summary': 'Summary',
        }
        error_messages = {
            'full_name': {
                'max_length': "This name is too long.",
            },
            'headline': {
                'max_length': "This headline is too long.",
            },
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['resume_file'].required = False

        # Hide moderation_status field entirely for non-staff or superuser
        if user and (not user.is_staff or user.is_superuser):
            self.fields.pop('moderation_status', None)

            
        

    def clean_resume_file(self):
        file = self.cleaned_data.get('resume_file', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("File too large. Size should not exceed 5 MB.")
        return file
