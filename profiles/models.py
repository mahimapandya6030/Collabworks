from django.db import models
from accounts.models import User
from skills.models import Skill

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    college = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    location  = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.user.username}"
    
class OrganizationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    department = models.CharField(max_length=100, blank=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    college = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
        