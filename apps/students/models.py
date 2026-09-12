from django.db import models
from django.conf import settings
from apps.schools.models import School
from apps.academics.models import AcademicYear, Class, Section
from apps.parents.models import ParentProfile # Will create this shortly

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    student_id = models.CharField(max_length=50, unique=True, help_text="Permanent Student ID")
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=50, blank=True)
    
    parents = models.ManyToManyField(ParentProfile, related_name='children', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"

class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, blank=True)
    
    status = models.CharField(max_length=20, choices=(('Active', 'Active'), ('Promoted', 'Promoted'), ('Dropped', 'Dropped')), default='Active')

    class Meta:
        unique_together = ('student', 'academic_year')
        
    def __str__(self):
        return f"{self.student} - {self.student_class} {self.section} ({self.academic_year})"
