from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import School
from django import forms

class SchoolSettingsForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'city', 'state', 'country', 'phone', 'email', 'website', 'principal_name', 'registration_info', 'primary_color', 'secondary_color']
        
class SchoolSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = School
    form_class = SchoolSettingsForm
    template_name = 'schools/school_settings.html'
    success_url = reverse_lazy('dashboard') # Redirect to dashboard or back to settings
    
    def get_object(self, queryset=None):
        # Always get or create the first school object for settings
        school, created = School.objects.get_or_create(id=1, defaults={'name': 'My School'})
        return school
