from django import forms
from .models import Skill

class skillform(forms.Form):
    new_skill = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add new skills', 'class': 'form-control'})
    )