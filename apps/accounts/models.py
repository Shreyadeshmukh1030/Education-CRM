from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived'),
    )
    
    phone = models.CharField(max_length=20, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
