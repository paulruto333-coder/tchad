from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a default superuser (admin/admin123) if one does not already exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                phone_number='0000000000',
                email='admin@admin.com',
            )
            self.stdout.write(self.style.SUCCESS(
                '[+] Default admin user created: username=admin, password=admin123'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '[*] Admin user already exists, skipping creation.'
            ))
