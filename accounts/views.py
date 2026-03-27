from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import StudentProfile, OrganizationProfile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from project.models import projectapplication, Project
from skills.models import Skill
from skills.forms import skillform
from django.db.models import Count
from django.contrib.auth import logout
from profiles.forms import StudentProfileForm, OrganizationProfileForm
import re
from django.contrib.auth import get_user_model
from django.db import IntegrityError


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not registered. Please sign up first.")
            return redirect('accounts:login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('project-list')
            

        else:
            messages.error(request, "Invalid credentials")
            return redirect('accounts:login')  
      

    return render(request, 'accounts/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  

        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'accounts/signup.html')
        
        
        if not re.search(r"[A-Z]", password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect('accounts:signup')

        if not re.search(r"[0-9]", password):
            messages.error(request, "Password must contain at least one number.")
            return redirect('accounts:signup')
        
        

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                role=role
            )
        except IntegrityError:
            messages.error(request, "Username already exists.")
            return redirect('accounts:signup')
        
        
        login(request, user)
        return redirect('accounts:login')
    
    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    return redirect('core:home')
    

@login_required
def profile_view(request):
    student_profile = None
    org_profile = None
    participated_obj = None
    projects = None

    role = request.user.role.strip().lower()
    
    if role == 'student':
        student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

        participated_obj = projectapplication.objects.filter(
            student=student_profile
        )

    elif role in ['club', 'faculty']:
        org_profile, created = OrganizationProfile.objects.get_or_create(user=request.user)

        projects = org_profile.pros.all()

    return render(request, 'accounts/my_profile.html', {
        'student_profile': student_profile,
        'org_profile': org_profile,
        'participated_obj': participated_obj,
        'projects': projects,
    })
 
# @login_required
# def user_profile_view(request, username):
#     user_obj = get_object_or_404(User, username=username)

#     viewer = request.user
#     viewer_role = viewer.role.strip().lower()
#     target_role = user_obj.role.strip().lower()

#     student_profile = None
#     org_profile = None
#     participated_obj = None
#     projects = None

#     allowed = False
#     print("clicked user:", user_obj.username)
#     print("role:", user_obj.role)
#     print("student_profile:", student_profile)
#     print("org_profile:", org_profile)

#     if viewer == user_obj:
#         allowed = True

#     elif target_role in ['club', 'faculty']:
#         allowed = True

#     elif viewer_role in ['club', 'faculty'] and target_role == 'student':
#         allowed = True

#     elif viewer_role == 'student' and target_role == 'student':
#         viewer_student = StudentProfile.objects.filter(user=viewer).first()
#         target_student = StudentProfile.objects.filter(user=user_obj).first()

#         if viewer_student and target_student:
#             same_project = projectapplication.objects.filter(
#                 student=viewer_student,
#                 status='ACCEPTED',
#                 project__applications__student=target_student,
#                 project__applications__status='ACCEPTED',
#             ).exists()

#             if same_project:
#                 allowed = True

#     if not allowed:
#         messages.error(
#             request,
#             "You can only view another student's profile if both of you are accepted in the same project."
#         )
#         return redirect('project-list')

#     if target_role == 'student':
#         student_profile, created = StudentProfile.objects.get_or_create(user=user_obj)
#         participated_obj = projectapplication.objects.filter(student=student_profile)

#     elif target_role in ['club', 'faculty']:
#         org_profile, created = OrganizationProfile.objects.get_or_create(user=user_obj)
#         projects = org_profile.pros.all()

#     return render(request, 'accounts/user_profile_view.html', {
#         'profile_user': user_obj,
#         'student_profile': student_profile,
#         'org_profile': org_profile,
#         'participated_obj': participated_obj,
#         'projects': projects,
#     })

User = get_user_model()


@login_required
def user_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)

    viewer = request.user
    viewer_role = viewer.role.strip().lower()
    target_role = user_obj.role.strip().lower()

    student_profile = None
    org_profile = None
    participated_obj = None
    projects = None

    # ----------------------------
    # DEBUG
    # ----------------------------
    print("viewer:", viewer.username, viewer.id, viewer.role)
    print("target username from url:", username)
    print("user_obj:", user_obj.username, user_obj.id, user_obj.role)

    print("student exists:", StudentProfile.objects.filter(user=user_obj).exists())
    print("org exists:", OrganizationProfile.objects.filter(user=user_obj).exists())

    # ----------------------------
    # PERMISSION CHECK
    # ----------------------------
    allowed = False

    # own profile
    if viewer == user_obj:
        allowed = True

    # everyone can see club/faculty profile
    elif target_role in ['club', 'faculty']:
        allowed = True

    # club/faculty can see student profile
    elif viewer_role in ['club', 'faculty'] and target_role == 'student':
        allowed = True

    # student can see another student only if both are accepted in same project
    elif viewer_role == 'student' and target_role == 'student':
        viewer_student = StudentProfile.objects.filter(user=viewer).first()
        target_student = StudentProfile.objects.filter(user=user_obj).first()

        print("viewer_student:", viewer_student)
        print("target_student:", target_student)

        if viewer_student and target_student:
            same_project = projectapplication.objects.filter(
                student=viewer_student,
                status='ACCEPTED',
                project__applications__student=target_student,
                project__applications__status='ACCEPTED'
            ).exists()

            print("same_project:", same_project)

            if same_project:
                allowed = True

    if not allowed:
        messages.error(
            request,
            "You can only view another student's profile if both of you are accepted in the same project."
        )
        return redirect('project-list')

    # ----------------------------
    # LOAD PROFILE DATA
    # ----------------------------
    if target_role == 'student':
        student_profile = StudentProfile.objects.filter(user=user_obj).first()

        if student_profile:
            participated_obj = projectapplication.objects.filter(student=student_profile)

    elif target_role in ['club', 'faculty']:
        org_profile = OrganizationProfile.objects.filter(user=user_obj).first()

        if org_profile:
            projects = org_profile.pros.all()

    print("final student_profile:", student_profile)
    print("final org_profile:", org_profile)

    return render(request, 'accounts/user_profile_view.html', {
        'profile_user': user_obj,
        'viewer_role': viewer_role,
        'target_role': target_role,
        'student_profile': student_profile,
        'org_profile': org_profile,
        'participated_obj': participated_obj,
        'projects': projects,
    })
 
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    role = request.user.role.strip().lower()

    student_profile = None
    org_profile = None
    student_form = None
    org_form = None
    active_members = None
    projects = None

    if role == 'student':
        student_profile, _ = StudentProfile.objects.get_or_create(user=request.user)

        student_form = StudentProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=student_profile
        )

        if request.method == 'POST':
            if student_form.is_valid():
                student_form.save()
                return redirect('accounts:edit_profile')
            else:
                print("STUDENT FORM ERRORS:", student_form.errors)

    elif role in ['club', 'faculty']:
        org_profile, _ = OrganizationProfile.objects.get_or_create(user=request.user)

        projects = Project.objects.filter(created_by=org_profile)

        active_members = (
            projectapplication.objects.filter(
                project__created_by=org_profile,
                status='ACCEPTED',
            )
            .values('student__user__username')
            .annotate(project_count=Count('project', distinct=True))
        )

        org_form = OrganizationProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=org_profile
        )

        if request.method == 'POST':
            if org_form.is_valid():
                org_form.save()
                return redirect('accounts:edit_profile')
            else:
                print("ORG FORM ERRORS:", org_form.errors)

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'student_profile': student_profile,
            'org_profile': org_profile,
            'student_form': student_form,
            'org_form': org_form,
            'active_members': active_members,
            'projects': projects,
        }
    )

def add_skill(request):
    if request.method == "POST":
        skill_name = request.POST.get('skill')

        skill, created = Skill.objects.get_or_create(name=skill_name)

        request.user.studentprofile.skills.add(skill)

        return redirect('edit_profile')


    