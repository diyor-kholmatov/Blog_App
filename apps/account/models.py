from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError('Email did not come')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not password:
            raise TypeError('Password did not come')
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Active user')
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_admin = models.BooleanField(default=False, verbose_name='Admin user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    date_login = models.DateTimeField(auto_now=True, verbose_name='Last login')
    date_create = models.DateField(auto_now=True, verbose_name='Create date')

    objects = AccountManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.first_name}'
        return f'{self.email}'

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data