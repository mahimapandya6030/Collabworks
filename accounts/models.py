from django.db import models
from django.contrib.auth.models import AbstractUser,  Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'student'),
        ('CLUB', 'club'),
        ('FACULTY', 'faculty'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


    groups = models.ManyToManyField(
        Group,
        related_name="collabworks_user",
        blank = True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="collabworks_users_permission",
        blank= True
    )
    
    def is_student(self):
        return self.role == 'STUDENT'

    def is_club(self):
        return self.role == 'CLUB'

    def is_faculty(self):
        return self.role == 'FACULTY'