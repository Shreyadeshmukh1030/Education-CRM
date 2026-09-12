from django.db import models
from django.conf import settings
from apps.schools.models import School

class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    employee_id = models.CharField(max_length=50, unique=True)
    
    department = models.CharField(max_length=100, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    
    # We will add ManyToMany for subjects and classes later when Subject model is created
    classes = models.ManyToManyField('academics.Class', related_name='assigned_teachers', blank=True)
    subjects = models.ManyToManyField('academics.Subject', related_name='assigned_teachers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.employee_id})"
