from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, date_of_birth, profile_photo):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not date_of_birth:
            raise ValueError('Users must have a date of birth')
        if not profile_photo:
            raise ValueError('Users must have a profile photo')
       
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            profile_photo=profile_photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        # Set default values for required fields if not provided
        if 'date_of_birth' not in extra_fields:
            extra_fields['date_of_birth'] = '2000-01-01'  # Default date
        if 'profile_photo' not in extra_fields:
            extra_fields['profile_photo'] = 'default.jpg'  # Default photo

        user = self.create_user(
            username=username,
            email=email,
            password=password,
            date_of_birth=extra_fields.get('date_of_birth'),
            profile_photo=extra_fields.get('profile_photo')
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(blank=False, null=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=False, null=False)
    objects = CustomUserManager()