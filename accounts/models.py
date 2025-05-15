# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

EMPLOYMENT_CHOICES = [
    ("full_time", "Full Time"),
    ("part_time", "Part Time"),
    ("intern", "Intern"),
]


class CustomUser(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_CHOICES, blank=True
    )
    access_level = models.CharField(max_length=50, blank=True)
    supervisor = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    date_of_joining = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username"
    ]  # still required by Django, use dummy username in logic

    def __str__(self):
        return self.email
