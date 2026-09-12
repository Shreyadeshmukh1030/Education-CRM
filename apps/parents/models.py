from django.db import models
from django.conf import settings
from apps.schools.models import School

class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='parents')
    
    occupation = models.CharField(max_length=100, blank=True)
    relationship_to_student = models.CharField(max_length=50, blank=True, help_text="e.g., Father, Mother, Guardian")
    address = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
