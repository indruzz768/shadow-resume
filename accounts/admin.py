from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'is_superuser', 'profile_photo']
    list_filter = ('role',)
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role', 'profile_photo')}),
    )

admin.site.register(User, CustomUserAdmin)
