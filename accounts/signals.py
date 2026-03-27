from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from profiles.models import StudentProfile, OrganizationProfile


user = get_user_model()

@receiver(post_save, sender=user)
def create_profile(sender, instance, created, **kwargs): 
    print("SIGNAL FIRED", instance.username, instance.role, created)
    if not created:
        return
    
    role = instance.role.strip().lower()

    if role == 'student':
        StudentProfile.objects.get_or_create(user=instance)
        print("Student profile created")

    elif role in ['club', 'faculty']:
        OrganizationProfile.objects.get_or_create(user=instance)    
        print("org profile created")
