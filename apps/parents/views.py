from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ParentProfile
from django.contrib.auth.models import User
from django import forms
from apps.schools.models import School

class ParentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = ParentProfile
        fields = ['occupation', 'relationship_to_student', 'address']

    def save(self, commit=True):
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
        
        if commit:
            parent.save()
            
        return parent

class ParentListView(LoginRequiredMixin, ListView):
    model = ParentProfile
    template_name = 'parents/parent_list.html'
    context_object_name = 'parents'
    
    def get_queryset(self):
        return ParentProfile.objects.select_related('user').all()

class ParentCreateView(LoginRequiredMixin, CreateView):
    model = ParentProfile
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')
