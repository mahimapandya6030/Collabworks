from django.urls import path
from .views import project_detail, view_applicants, project_list, create_project, apply_project, my_applications, application_status, edit_project, all_applications, remove_student_from_project
from applications.views import projectapplicationview


urlpatterns = [
    path('create_project/', create_project, name='create_project'),
    path('projects/', project_list, name='project-list'),
    path('projects/<int:pk>/applypro/', apply_project, name='apply_project'),
    path('projects/<int:project_id>/applicants/', projectapplicationview.as_view()),
    path('projects/<int:project_id>/applicant/', view_applicants, name='applicants'),
    path('projects/<int:project_id>/', project_detail, name='project_detail'),
    path('projects/my_applications/', my_applications, name='my_applications'),
    path('projects/all_applications/', all_applications, name='all_applications'),
    path('projects/<int:app_id>/update/<str:action>/', application_status, name='application_status'),
    path('projects/<int:project_id>/edit/', edit_project, name='edit_project'),
   path(
    'projects/<int:project_id>/remove-student/<int:application_id>/',remove_student_from_project,
    name='remove_student_from_project'
),
    
]