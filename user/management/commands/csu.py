from django.core.management import BaseCommand

from user.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.com',
            first_name='Admin',
            last_name='Kr_py',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('200818')
        user.save()