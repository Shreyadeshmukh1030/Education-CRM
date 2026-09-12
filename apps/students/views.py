from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StudentProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'date_of_birth', 'gender', 'blood_group', 'admission_date', 'address', 'emergency_contact']

    def save(self, commit=True):
        # We need to create a user first
        user = User.objects.create_user(
            username=self.cleaned_data['email'], # using email as username
            email=self.cleaned_data['email'],
            password='defaultpassword123', # In a real app, generate this or email a reset link
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        student = super().save(commit=False)
        student.user = user
        # For simplicity, just get the first school or default
        school = School.objects.first()
        student.school = school
        
        if commit:
            student.save()
            
        return student

class StudentListView(LoginRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    
    def get_queryset(self):
        # Optionally filter by school if implemented
        return StudentProfile.objects.select_related('user').all()

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
