from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    '''
    Custom User model where email is the unique identifiers
    '''
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        ''' Return email as string representation '''
        return self.email
    
    class Meta:                
        verbose_name = 'User'
        verbose_name_plural = 'Users'
