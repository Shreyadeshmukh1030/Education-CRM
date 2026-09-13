from django.db import models
from apps.schools.models import School
from apps.academics.models import Class
from django.conf import settings

class Lead(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Interested', 'Interested'),
        ('Follow-up', 'Follow-up'),
        ('Application Started', 'Application Started'),
        ('Application Submitted', 'Application Submitted'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
        ('Admitted', 'Admitted'),
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='leads')
    student_name = models.CharField(max_length=255)
    parent_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    interested_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    notes = models.TextField(blank=True)
    assigned_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.status}"

class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='followups')
    date = models.DateField()
    notes = models.TextField()
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AdmissionApplication(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, related_name='application')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='applications')
    application_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    previous_school = models.CharField(max_length=255, blank=True)
    documents_submitted = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"App: {self.application_number} ({self.lead.student_name})"
