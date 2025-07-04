from django.core.management.base import BaseCommand
from accounts.models import User  # adjust if your user model is elsewhere

class Command(BaseCommand):
    help = 'Promote a user to admin status'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.role = 'admin'  # if using a custom role field
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ {username} is now an admin.'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User "{username}" not found.'))
