from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project, ProjectApplication
from django.shortcuts import render, get_object_or_404

class projectapplicationview(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)

        # Only creator can see
        if project.owner != request.user:
            return Response({"error": "Not allowed"}, status=403)

        applications = project.applications.select_related('student')

        data = [
            {
                "student_id": app.student.id,
                "student_name": app.student.username,
                "applied_at": app.applied_at
            }
            for app in applications
        ]

        return Response(data)
    

