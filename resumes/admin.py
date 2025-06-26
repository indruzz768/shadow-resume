from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'moderation_status', 'status', 'created_at','public_uuid')
    list_filter = ('moderation_status', 'status', 'created_at', 'user')
    search_fields = ('full_name', 'user__username', 'headline', 'skills', 'summary',)
    ordering = ('-created_at',)
    readonly_fields = ('public_uuid', 'created_at')


    # ✅ Custom actions for bulk moderation
    actions = ['mark_as_approved', 'mark_as_rejected']

    @admin.action(description='✅ Approve selected resumes')
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(moderation_status='approved')
        self.message_user(request, f"{updated} resume(s) approved.")

    @admin.action(description='❌ Reject selected resumes')
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(moderation_status='rejected')
        self.message_user(request, f"{updated} resume(s) rejected.")