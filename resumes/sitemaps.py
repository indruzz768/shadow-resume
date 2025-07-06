from django.contrib.sitemaps import Sitemap
from .models import Resume

class ResumeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Resume.objects.filter(moderation_status='approved')

    def location(self, obj):
        return f"/r/{obj.public_uuid}/"
