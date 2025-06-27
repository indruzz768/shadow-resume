from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Password reset views
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Admin and app routes
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('resumes/', include('resumes.urls')),
    path('api/', include('resumes.api_urls')),
    path('ai/', include('ai_service.urls')),
    path('accounts/', include('allauth.urls')),

    # Admin dashboard
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Default root redirect
    path('', RedirectView.as_view(url='/resumes/', permanent=False)),
]

# Media file support in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
