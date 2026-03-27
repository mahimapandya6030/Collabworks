from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project, projectapplication
from profiles.models import StudentProfile
from .serializer import Projectapplication_serializer, Projectapplications_serializer, myapplication_serializer
from .permissions import Iscluborfaculty, Isstudent


class projectlist_api(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = Projectapplication_serializer
    permission_classes = [AllowAny]
   
    
class Projectcreate_apiview(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = Projectapplication_serializer
    permission_classes = [IsAuthenticated, Iscluborfaculty]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)    
        
class applyproject_apiview(CreateAPIView):
    queryset = projectapplication.objects.all()
    serializer_class = Projectapplications_serializer
    permission_classes = [IsAuthenticated, Isstudent]
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user.studentprofile)
             
             
class projectapplicants_apiview(ListAPIView):
    serializer_class = Projectapplications_serializer
    permission_classes = [IsAuthenticated, Iscluborfaculty]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return projectapplication.objects.filter(project_id=project_id)              
    
class  updateapplications_apiview(UpdateAPIView):
    queryset = projectapplication.objects.all()
    serializer_class = Projectapplications_serializer
    permission_classes = [IsAuthenticated, Iscluborfaculty]
    http_method_names = ['patch']
    
    def perform_update(self, serializer):
        serializer.save() 
        
        
class myapplication_apiview(ListAPIView):
    serializer_class = myapplication_serializer
    permission_classes = [IsAuthenticated, Isstudent]
    
    def get_queryset(self):
        return projectapplication.objects.filter(
            student=self.request.user.studentprofile
        )        
        
        
        
        