from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import CommandError
from django.core.management import CommandParser
from datetime import datetime

class Command(createsuperuser.Command):
    help = 'Creates a superuser with all required fields'

    def handle(self, *args, **options):
        username = input('Username: ')
        email = input('Email address: ')
        date_of_birth = input('Date of birth (YYYY-MM-DD): ')
        profile_photo = input('Profile photo path: ')
        password = None

        # Validate date format
        try:
            datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            raise CommandError('Date must be in YYYY-MM-DD format')

        while password is None:
            password = input('Password: ')
            password2 = input('Password (again): ')
            if password != password2:
                self.stderr.write("Error: Your passwords didn't match.")
                password = None
                continue

        try:
            user = self.UserModel._default_manager.create_superuser(
                username=username,
                email=email,
                password=password,
                date_of_birth=date_of_birth,
                profile_photo=profile_photo
            )
            if options.get('verbosity', 1) >= 1:
                self.stdout.write(self.style.SUCCESS(f"Superuser '{user.username}' created successfully."))
        except Exception as e:
            raise CommandError(str(e))
