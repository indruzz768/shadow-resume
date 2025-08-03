from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from cloudinary.models import CloudinaryField  # Ensure Cloudinary is installed
from django.utils.translation import gettext_lazy as _

class User(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_staff = models.BooleanField(default=False)  # Controls staff site access (auto-set in save)
    github_skills = models.JSONField(default=list, blank=True, null=True)
    github_projects = models.JSONField(default=list, blank=True, null=True)
    profile_photo = CloudinaryField('profile_photo', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically set is_staff based on role
        self.is_staff = self.role in ['admin', 'staff']
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return self.username
