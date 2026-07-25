from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the production admin superuser."

    def handle(self, *args, **options):
        User = get_user_model()
        username = "admin"
        password = "admin1234@"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
                "email": "",
            },
        )

        if not created:
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True

        user.set_password(password)
        user.save()

        state = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Superuser {state}: {username}"))