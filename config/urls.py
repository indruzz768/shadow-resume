from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views
from django.views.generic import RedirectView
from resumes.views import public_resume_view # Import the public resume view
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from resumes.sitemaps import ResumeSitemap

handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'

# Sitemap configuration
sitemaps = {
    'resumes': ResumeSitemap,
}


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
    path('integrations/', include('integrations.urls')),

    # Admin dashboard
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Default root redirect
    path('', RedirectView.as_view(url='/resumes/', permanent=False)),
    # Public resume view
    path('r/<uuid:uuid>/', public_resume_view, name='public_resume'),
    
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]

# Media file support in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
