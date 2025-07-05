from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid
from django.core.files.storage import default_storage

User = get_user_model()



class Resume(models.Model):
    MODERATION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # Moderation status for the resume
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES, default='pending')

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('rejected', 'Rejected'),
        ('job_ready', 'Job Ready'),
        ('private', 'Private'),
    ]
    public_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    address = models.CharField(max_length=255, blank=True)
    headline = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(help_text="Comma-separated skills", blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resume_file = models.FileField(upload_to='resumes/files/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f"{self.user.email} - {self.full_name}"

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.status:
            self.status = self.status.strip()
        if self.moderation_status:
            self.moderation_status = self.moderation_status.strip()
        super().save(*args, **kwargs)

    @property
    def has_resume_file(self):
        return self.resume_file and default_storage.exists(self.resume_file.name)
