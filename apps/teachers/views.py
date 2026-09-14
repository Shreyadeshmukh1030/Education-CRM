from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TeacherProfile
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from apps.accounts.mixins import RoleRequiredMixin, SchoolIsolationMixin
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
            # School will be assigned in form_valid or views instead of here
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

class TeacherListView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, ListView):
    model = TeacherProfile
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    allowed_roles = ['Admin']
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('user')

class TeacherDetailView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DetailView):
    model = TeacherProfile
    template_name = 'teachers/teacher_detail.html'
    context_object_name = 'teacher'
    allowed_roles = ['Admin']

class TeacherCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = TeacherProfile
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['Admin']

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class TeacherUpdateView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['Admin']

class TeacherDeleteView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DeleteView):
    model = TeacherProfile
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')
    allowed_roles = ['Admin']

class TeacherMyClassesView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    template_name = 'teachers/my_classes.html'
    context_object_name = 'classes'
    allowed_roles = ['Teacher']
    
    def get_queryset(self):
        teacher = self.request.user.teacher_profile
        return teacher.classes.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.teacher_profile
        context['counselor_for_class'] = getattr(teacher, 'counselor_for_class', None)
        return context

from apps.academics.models import Class
from apps.students.models import StudentProfile

class TeacherClassDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = Class
    template_name = 'teachers/class_detail.html'
    context_object_name = 'class_obj'
    allowed_roles = ['Teacher']
    
    def get_queryset(self):
        # Ensure the teacher is assigned to this class
        teacher = self.request.user.teacher_profile
        return teacher.classes.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get students in this class
        context['students'] = StudentProfile.objects.filter(current_class=self.object)
        teacher = self.request.user.teacher_profile
        context['is_counselor'] = getattr(teacher, 'counselor_for_class', None) == self.object
        return context
