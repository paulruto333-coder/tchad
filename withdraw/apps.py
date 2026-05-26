from django.apps import AppConfig


class WithdrawConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'withdraw'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_default_admin, sender=self)


def create_default_admin(sender, **kwargs):
    """
    Automatically creates a default superuser (admin/admin123) after migrations
    if one does not already exist. If the user already exists, ensures it has
    superuser privileges.
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                phone_number='0000000000',
                email='admin@admin.com',
            )
            print('[+] Default admin user created: username=admin, password=admin123')
        else:
            # Ensure existing admin has superuser privileges
            admin_user = User.objects.get(username='admin')
            updated = False
            if not admin_user.is_superuser:
                admin_user.is_superuser = True
                updated = True
            if not admin_user.is_staff:
                admin_user.is_staff = True
                updated = True
            if updated:
                admin_user.save()
                print('[*] Admin user updated with superuser privileges.')
            else:
                print('[*] Admin user already exists with correct privileges, skipping.')
    except Exception as e:
        print(f'[!] Could not create default admin user: {e}')
