from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StudentProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School
from apps.accounts.mixins import RoleRequiredMixin

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'date_of_birth', 'gender', 'blood_group', 'admission_date', 'address', 'emergency_contact', 'current_class']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['email'], # using email as username
                email=self.cleaned_data['email'],
                password='defaultpassword123',
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            student = super().save(commit=False)
            student.user = user
            school = School.objects.first()
            student.school = school
        else:
            student = super().save(commit=False)
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.email = self.cleaned_data['email']
            student.user.save()
            
        if commit:
            student.save()
            
        return student

class StudentListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    allowed_roles = ['admin', 'teacher']
    
    def get_queryset(self):
        user = self.request.user
        if 'admin' in user.role.name.lower():
            return StudentProfile.objects.select_related('user', 'current_class').all()
        elif 'teacher' in user.role.name.lower():
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                return StudentProfile.objects.filter(current_class__in=teacher.classes.all()).select_related('user', 'current_class')
        return StudentProfile.objects.none()

class StudentDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    allowed_roles = ['admin', 'teacher']

class StudentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['admin']

class StudentUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['admin']

class StudentDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = StudentProfile
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['admin']
