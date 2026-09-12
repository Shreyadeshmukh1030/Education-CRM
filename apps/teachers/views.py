from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TeacherProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'department', 'joining_date']

    def save(self, commit=True):
        # We need to create a user first
        user = User.objects.create_user(
            username=self.cleaned_data['email'], # using email as username
            email=self.cleaned_data['email'],
            password='defaultpassword123',
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        teacher = super().save(commit=False)
        teacher.user = user
        # For simplicity, just get the first school or default
        school = School.objects.first()
        teacher.school = school
        
        if commit:
            teacher.save()
            
        return teacher

class TeacherListView(LoginRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    
    def get_queryset(self):
        return TeacherProfile.objects.select_related('user').all()

class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = TeacherProfile
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')
