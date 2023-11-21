from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


#class AccountManager()

class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_login = models.DateTimeField(auto_now=True, verbose_name='Last login')


    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True,
                                    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                    related_query_name="customuser")
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True,
                                              help_text='Specific permissions for this user.',
                                              related_query_name="customuser")

