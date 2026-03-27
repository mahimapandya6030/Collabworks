from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import StudentProfile
from project.models import Project

def portfolio(request, username):
    student = StudentProfile.objects.get(user__username=username)
    projects = Project.objects.filter(
        applications__student=student,
        applications__status='ACCEPTED'
    )
    return render(request, 'profiles/portfolio.html',  {
        'student': student,
        'projects': projects,
    })




