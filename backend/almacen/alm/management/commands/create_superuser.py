from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nuve.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))
        else:
            # Update password if user exists
            user = User.objects.get(username='admin')
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser "admin" password updated'))
