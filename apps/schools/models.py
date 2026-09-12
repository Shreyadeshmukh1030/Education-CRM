from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    principal_name = models.CharField(max_length=255, blank=True)
    registration_info = models.TextField(blank=True)
    
    # Branding
    primary_color = models.CharField(max_length=7, default='#000000', help_text="Hex color code")
    secondary_color = models.CharField(max_length=7, default='#ffffff', help_text="Hex color code")
    
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SchoolUpdate(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='updates')
    
    def __str__(self):
        return self.title
