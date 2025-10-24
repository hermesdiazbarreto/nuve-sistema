from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='nuve').exists():
            User.objects.create_superuser('nuve', 'admin@nuve.com', 'nuve-123')
            self.stdout.write(self.style.SUCCESS('Superuser "nuve" created successfully'))
        else:
            # Update password if user exists
            user = User.objects.get(username='nuve')
            user.set_password('nuve-123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser "nuve" password updated'))
