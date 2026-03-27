from django.contrib import admin
from .models import StudentProfile, OrganizationProfile

admin.site.register(StudentProfile)
admin.site.register(OrganizationProfile)

