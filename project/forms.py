from django import forms
from .models import Project


class projectforms(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'team_size',
            'duration_weeks',
            'meeting_format',
            'status',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'meeting_format': forms.Select()
        }
        
  