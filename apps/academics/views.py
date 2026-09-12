from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Class
from apps.schools.models import School
from django import forms

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'order']

    def save(self, commit=True):
        class_instance = super().save(commit=False)
        school = School.objects.first()
        class_instance.school = school
        if commit:
            class_instance.save()
        return class_instance

class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'academics/class_form.html'
    success_url = reverse_lazy('class_list')

from .models import Assignment, StudyMaterial

class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'academics/assignment_list.html'
    context_object_name = 'assignments'
    ordering = ['-due_date']

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'academics/assignment_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'due_date', 'max_marks', 'attachment']
    success_url = reverse_lazy('assignment_list')

class StudyMaterialListView(LoginRequiredMixin, ListView):
    model = StudyMaterial
    template_name = 'academics/material_list.html'
    context_object_name = 'materials'
    ordering = ['-uploaded_at']

class StudyMaterialCreateView(LoginRequiredMixin, CreateView):
    model = StudyMaterial
    template_name = 'academics/material_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'topic', 'file']
    success_url = reverse_lazy('material_list')
