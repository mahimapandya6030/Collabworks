from .models import StudentProfile, OrganizationProfile
from django import forms



class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'resume',
            'college',
            'department',
            'branch',
            'year',
            'bio',
            'email',
            'phone_num',
            'location',
        ]

        


class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = [
            'email',
            'phone_num',
            'location',
            'description',
            'college',
            'department',
            'branch',
            'github',
            'linkedin',
        ]
                