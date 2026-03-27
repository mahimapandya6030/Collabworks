from django.shortcuts import render
from project.models import Project, projectapplication
from project.filters import ProjectFilter
from django.shortcuts import render, get_object_or_404
from profiles.models import OrganizationProfile

def home(request):
    projects = Project.objects.all()

    project_filter = ProjectFilter(request.GET, queryset=projects)

    team_members = projectapplication.objects.filter(
        status='ACCEPTED'
    ).values('student').distinct().count()

    return render(request, 'core/home.html', {
        'project_filter': project_filter,
        'team_members': team_members,
    })
    