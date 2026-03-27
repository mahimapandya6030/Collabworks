from rest_framework import serializers
from .models import projectapplication, Project

class Projectapplication_serializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['student']
        
        
class Projectapplications_serializer(serializers.ModelSerializer):
    class Meta:
        model = projectapplication
        fields = '__all__'
        read_only_fields = ['student']    
        
        
class myapplication_serializer(serializers.ModelSerializer):
    project_title  = serializers.CharField(
        source = 'project.title',
        read_only = True
    )            
    
    class Meta:
        model = projectapplication
        fields = [
            'id',
            'project_title',
            'status',
            'applied_at'
        ]