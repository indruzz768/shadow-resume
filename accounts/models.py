from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    def is_admin(self):
        return self.role == 'admin'

    def is_user(self):
        return self.role == 'user'

    def save(self, *args, **kwargs):
        # Automatically set is_staff based on role
        self.is_staff = self.role in ['admin', 'staff']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
