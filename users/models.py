from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="default.jpg", upload_to="users")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    