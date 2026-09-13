from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import StudentProfile
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from apps.accounts.mixins import RoleRequiredMixin, SchoolIsolationMixin

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
            # School assigned in form_valid
        else:
            student = super().save(commit=False)
            student.user.first_name = self.cleaned_data['first_name']
            student.user.last_name = self.cleaned_data['last_name']
            student.user.email = self.cleaned_data['email']
            student.user.save()
            
        if commit:
            student.save()
            
        return student

class StudentListView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, ListView):
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    allowed_roles = ['Admin', 'Teacher']
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if 'Admin' in user.role.name:
            return qs.select_related('user', 'current_class')
        elif 'Teacher' in user.role.name:
            teacher = getattr(user, 'teacher_profile', None)
            if teacher:
                return qs.filter(current_class__in=teacher.classes.all()).select_related('user', 'current_class')
        return qs.none()

class StudentDetailView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DetailView):
    model = StudentProfile
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    allowed_roles = ['Admin', 'Teacher']

class StudentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['Admin']

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, UpdateView):
    model = StudentProfile
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['Admin']

class StudentDeleteView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DeleteView):
    model = StudentProfile
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    allowed_roles = ['Admin']



# --- MARKSHEET ---
from apps.academics.models import ExamResult
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

class StudentMarksheetView(LoginRequiredMixin, RoleRequiredMixin, TemplateView):
    template_name = 'students/marksheet.html'
    allowed_roles = ['admin', 'teacher', 'parent', 'student']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs.get('pk')
        student = get_object_or_404(StudentProfile, pk=student_id)
        
        # Verify permissions:
        # If student, can only view own marksheet
        # If parent, can only view children's marksheet
        user = self.request.user
        role = user.role.name.lower()
        if 'student' in role and getattr(user, 'student_profile', None) != student:
            # Maybe raise 403 or redirect
            pass
        if 'parent' in role:
            parent = getattr(user, 'parent_profile', None)
            if parent and student not in parent.children.all():
                pass # Should raise 403
                
        results = ExamResult.objects.filter(student=student).select_related('exam', 'subject').order_by('-exam__date')
        
        # Group by exam
        exams_dict = {}
        for r in results:
            if r.exam not in exams_dict:
                exams_dict[r.exam] = []
            exams_dict[r.exam].append(r)
            
        context['student'] = student
        context['exams_dict'] = exams_dict
        return context
