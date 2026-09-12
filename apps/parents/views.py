from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ParentProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School
from apps.accounts.mixins import RoleRequiredMixin

class ParentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = ParentProfile
        fields = ['occupation', 'relationship_to_student', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        if not self.instance.pk:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password='defaultpassword123',
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            
            parent = super().save(commit=False)
            parent.user = user
            school = School.objects.first()
            parent.school = school
        else:
            parent = super().save(commit=False)
            parent.user.first_name = self.cleaned_data['first_name']
            parent.user.last_name = self.cleaned_data['last_name']
            parent.user.email = self.cleaned_data['email']
            parent.user.save()
            
        if commit:
            parent.save()
            
        return parent

class ParentListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = ParentProfile
    template_name = 'parents/parent_list.html'
    context_object_name = 'parents'
    allowed_roles = ['admin']
    
    def get_queryset(self):
        return ParentProfile.objects.select_related('user').all()

class ParentDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    model = ParentProfile
    template_name = 'parents/parent_detail.html'
    context_object_name = 'parent'
    allowed_roles = ['admin']

class ParentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = ParentProfile
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['admin']

class ParentUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = ParentProfile
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['admin']

class ParentDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    model = ParentProfile
    template_name = 'parents/parent_confirm_delete.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['admin']
