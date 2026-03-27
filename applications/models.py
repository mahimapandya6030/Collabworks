from django.db import models
from profiles.models import StudentProfile
from project.models import Project

class ProjectApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    motivation = models.TextField()
    status = models.CharField(max_length=10)
    
    
class PortfolioItem(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contibution = models.TextField()
    verified = models.BooleanField(default=False)
    
    



