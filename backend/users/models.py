from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
class customUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def validate_password(self, password):
        try:
            validate_password(password, self)
        except ValidationError as error:
            raise ValueError(str(error))

    def set_password(self, raw_password):
        self.validate_password(raw_password)
        super().set_password(raw_password)

@receiver(post_save, sender=customUser)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Activate your account'
        message = 'Please click the following link to activate your account: {}/users/activate/{}'.format(
            settings.BASE_URL, instance.id
        )
        print(subject,message)
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])