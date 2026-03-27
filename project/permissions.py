from rest_framework.permissions import BasePermission


class Iscluborfaculty(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role in ['CLUB', 'FACULTY'])
    
    
class Isstudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'   