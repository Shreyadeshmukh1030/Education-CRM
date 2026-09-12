from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TeacherProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School
from apps.accounts.mixins import RoleRequiredMixin

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = TeacherProfile
        fields = ['employee_id', 'department', 'joining_date', 'classes', 'subjects']

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
            teacher = super().save(commit=False)
            teacher.user = user
            school = School.objects.first()
            teacher.school = school
        else:
            teacher = super().save(commit=False)
            teacher.user.first_name = self.cleaned_data['first_name']
            teacher.user.last_name = self.cleaned_data['last_name']
            teacher.user.email = self.cleaned_data['email']
            teacher.user.save()
            
        if commit:
            teacher.save()
            # save_m2m is needed for ManyToMany fields (classes, subjects) when commit=False
            self.save_m2m()
            
        return teacher

class TeacherListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = TeacherProfile
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    allowed_roles = ['admin']
    
    def get_queryset(self):
        return TeacherProfile.objects.select_related('user').all()

class TeacherDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = TeacherProfile
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'
    allowed_roles = ['admin']

class TeacherCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = TeacherProfile
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['admin']

class TeacherUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['admin']

class TeacherDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = TeacherProfile
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['admin']
