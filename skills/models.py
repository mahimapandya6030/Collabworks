from django.db import models

class Skill(models.Model):
   
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('TECH', 'Technical Skills'),
            ('SOFT', 'Soft Skills'),
            ('TOOLS', 'Tools & Technologies'),
        ]
    )
    def __str__(self):
        return f"{self.name}"