from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Project, projectapplication
from .models import Project, projectapplication
from profiles.models import OrganizationProfile
from skills.models import Skill
from .filters import ProjectFilter
from django.shortcuts import render, get_object_or_404
from .forms import projectforms
from django.contrib import messages
from profiles.models import OrganizationProfile, StudentProfile
from django.db.models import Count
from .forms import projectforms
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator



@login_required
def create_project(request):
    print("METHOD:", request.method)
    if request.user.role.strip().lower() not in ['CLUB', 'FACULTY']:
        messages.error(request, "Access denied. Only faculty or club  can create projects.")
        return redirect('core:home')
    
    org_profile = get_object_or_404(OrganizationProfile, user=request.user)
    
    if request.method == 'POST':
        print("POST DATA:", request.POST)

        form = projectforms(request.POST)

        if form.is_valid():
            print("FORM IS VALID")

            project = form.save(commit=False)
            # org_profile = OrganizationProfile.objects.get(user=request.user)
            project.owner = org_profile
            project.created_by = org_profile
                
            project.save()  

            skill_names = request.POST.getlist('required_skills')
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name.strip())
                project.required_skills.add(skill)

            print("PROJECT SAVED")
            return redirect('project-list')

        else:
            print(form.errors)
      
    else:
        form = projectforms()
    
    return render(request, 'projects/create_project.html', {'form': form})    
    
    

def apply_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    
    if request.user.is_superuser:
        return HttpResponseForbidden("Admins cannot apply to projects")
        
    if request.user.role.strip().lower() != 'student':
        return HttpResponseForbidden("only students can apply")
    
    
    print("Logged in user:", request.user)
    print("User role:", request.user.role)
  
    
    student_profile = StudentProfile.objects.filter(user=request.user).first()
    if not student_profile:
        messages.error(request, "student profile does not exist.")
        return redirect("project_detail", pk)
    
    if projectapplication.objects.filter(
        project=project,
        student=student_profile,
    ).exists():
        messages.warning(request, "You have already applied to this project.")
        return redirect('project_detail', project_id=pk)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        try:
            projectapplication.objects.create(
                project=project,
                student=student_profile,
                message=message, 
                status='PENDING',
            )
            messages.success(request, "Application submitted successfully!")
        except IntegrityError:
            messages.warning(request, "You have already applied.")

    return redirect('project_detail', project_id=pk)


      
def project_list(request):
    projects = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'project_filter':project_filter,
    })
    
    
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    student_profile = None
    application = None
  
   
    if request.user.is_authenticated and request.user.role.strip().lower() == 'student':
        student_profile = StudentProfile.objects.filter(user=request.user).first()
        if student_profile:
            application = projectapplication.objects.filter(
                project=project,
                student=student_profile
            ).first()
            
    
    
    accepted_students = projectapplication.objects.filter(
        project=project,
        status='ACCEPTED'
    )       

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'application':application,
        'accepted_students':accepted_students,
    })    
    
    
def view_applicants(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner.user:
        return render(request, 'projects/not_allowed.html')

    org_pro = OrganizationProfile.objects.get(user=request.user)
    
    projects = Project.objects.filter(created_by=org_pro)
    applications = projectapplication.objects.filter(project=project)

    active_members = (
        projectapplication.objects.filter(
            project__created_by = org_pro,   # fr key
            status='ACCEPTED',
        )
        .values(
            'student__user__username',
            'student__department'
        )
        .annotate(project_count=Count('project', distinct=True))
    )
    
    active_projects = Project.objects.filter(
        created_by = org_pro
    ).exclude(status='COMPLETED').count()
    
    completed_projects = Project.objects.filter(
        created_by = org_pro,
        status='COMPLETED',
    ).count()
    
    in_progress = Project.objects.filter(
        created_by = org_pro,
        applications__status = 'ACCEPTED',
    ).distinct().count()
    
    team_members = projectapplication.objects.filter(
        project__created_by = org_pro,
        status='ACCEPTED'
    ).values('student').distinct().count()
    
    return render(request, 'projects/organization_dashboard.html', {
        'project': project,
        'applications': applications,
        'projects':projects,
        'active_members':active_members,
        'active_projects':active_projects,
        'completed_projects':completed_projects,
        'in_progress':in_progress,
        'team_members':team_members,
    })        
    
@login_required    
def my_applications(request):
    if request.user.role.strip().lower() != 'student': 
        return render(request, 'projects/not_allowed.html')

    
    student_profile = StudentProfile.objects.get(user=request.user)
    applications = projectapplication.objects.filter(student=student_profile).select_related('project').order_by('-applied_at')
    
    profile_fields = [
        student_profile.college,
        student_profile.branch,
        student_profile.skills,
        student_profile.resume,
        student_profile.bio,
    ]
    
    completed = sum(1 for field in profile_fields if field)
    profile_progress = int((completed / len(profile_fields)) * 100)
    
    paginator = Paginator(applications, 4)   # 4 applications per page
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'student': student_profile,
        'applications': applications,
        'pending_count': applications.filter(status='PENDING').count(),
        'accepted_count':applications.filter(status='ACCEPTED').count(),
        'rejected_count':applications.filter(status='REJECTED').count(),
        'completed_count':applications.filter(status='COMPLETED').count(),
        'profile_progress': profile_progress,
        'applications_page': applications_page,
    }
       
          
    return render(request, 'projects/student_dashboard.html', context)
    
def all_applications(request):
    projects = Project.objects.all()
    project_filter = ProjectFilter(request.GET, queryset=projects)
    student_profile = StudentProfile.objects.filter(user=request.user).first()

    applications = projectapplication.objects.filter(student=student_profile,
                                                     status='COMPLETED').select_related('project').order_by('-applied_at')


    return render(request, 'projects/all_applications.html', {
        'projects': projects,
        'project_filter':project_filter,
        'student_profile':student_profile,
        'applications': applications,
        'pending_count': applications.filter(status='PENDING').count(),
        'accepted_count':applications.filter(status='ACCEPTED').count(),
        'rejected_count':applications.filter(status='REJECTED').count(),
        'completed_count':applications.filter(status='COMPLETED').count(),
    })
   
    
def application_status(request, app_id, action):
    application = get_object_or_404(projectapplication, id=app_id)
    
    if request.user != application.project.created_by:
        messages.error(request, "not allowed")
        
    
    if action == 'accept':
        application.status = 'ACCEPTED'
        messages.success(request, "student accepted")
        
    elif action == 'reject':
        application.status = 'REJECTED'
        messages.success(request, "student rejected")
        
    elif action == 'complete':
        application.status = 'COMPLETED'
        messages.success(request, "project completed")
        
    else:
        messages.error(request, "Invalid action")
        return redirect('login')
    
    application.save()
    return redirect('applicants', application.project.id)            

    
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.created_by.user != request.user:
        print(project.created_by.user)
        return redirect('core:home')

    accepted_students = projectapplication.objects.filter(
        project=project,
        status='ACCEPTED'
    ).select_related('student__user')
    
    
    if request.method == 'POST':
        form = projectforms(request.POST, instance=project)
        print(form.errors)

        if form.is_valid():
            form.save()
            
            skill_input = request.POST.get("skills", "")
            skill_names = [s.strip() for s in skill_input.split(",") if s.strip()]
            
            skill_add = []
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                skill_add.append(skill)
            
            project.required_skills.set(skill_add)
            return redirect('project_detail', project_id=project.id)
    else:
        form = projectforms(instance=project)

    return render(request, 'projects/edit_project.html', {
        'form': form,
        'project': project,
        'accepted_students': accepted_students,
       
    })    
    


# def remove_student_from_project(request, project_id, application_id):
#     project = get_object_or_404(Project, id=project_id)

#     if not project.created_by or project.created_by.user != request.user:
#         return redirect('core:home')

#     application = get_object_or_404(
#         projectapplication,
#         id=application_id,
#         project=project
#     )

#     application.status = 'REMOVED'
#     application.delete()
#     application.save()

#     return redirect('project_detail', project_id=project.id)
        
        
def remove_student_from_project(request, project_id, application_id):
    project = get_object_or_404(Project, id=project_id)

    if not project.created_by or project.created_by.user != request.user:
        return redirect('core:home')

    application = get_object_or_404(
        projectapplication,
        id=application_id,
        project=project
    )

    application.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))        