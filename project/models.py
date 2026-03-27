from django.db import models
from profiles.models import OrganizationProfile, StudentProfile
from accounts.models import User
from skills.models import Skill
from django.conf import settings

class Project(models.Model):
    MEETING_CHOICES = [
        ('ONLINE', 'online'),
        ('IN_PERSON', 'in person'),
        ('HYBRID', 'hybrid'),
    ]
    owner = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE, related_name='pros')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skill)
    duration_weeks = models.IntegerField()
    team_size = models.IntegerField()
    status = models.CharField(max_length=15)
    meeting_format = models.CharField(
        max_length=20,
        choices=MEETING_CHOICES
    )
    created_by = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class projectapplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'completed'),
        ('REMOVED', 'removed'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="project_applications")  
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'student')
        
    def __str__(self):
        return f"{self.student.user.username} -> {self.project.title}"    
      