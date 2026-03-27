from django.urls import path
from .api_views import projectlist_api, Projectcreate_apiview, applyproject_apiview, projectapplicants_apiview, updateapplications_apiview, myapplication_apiview

urlpatterns = [
    path('projects/', projectlist_api.as_view()),
    path('projects/create/', Projectcreate_apiview.as_view()),
    path('projects/apply/', applyproject_apiview.as_view()),
    path('projects/<int:project_id>/applicants/', projectapplicants_apiview.as_view()),
    path('projects/<int:pk>/status/', updateapplications_apiview.as_view()),
    path('projects/myapplications/', myapplication_apiview.as_view()),

]
