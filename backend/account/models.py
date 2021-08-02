from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager
from project.models import ProjectModel


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20, unique=True)
    uuid = models.UUIDField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    ROLE_CHOICES = (
        ("user", "User"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    project = models.ManyToManyField(ProjectModel)

    USERNAME_FIELD = "uuid"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
