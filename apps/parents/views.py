from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ParentProfile
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from apps.accounts.mixins import RoleRequiredMixin, SchoolIsolationMixin
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
            # School assigned in form_valid
        else:
            parent = super().save(commit=False)
            parent.user.first_name = self.cleaned_data['first_name']
            parent.user.last_name = self.cleaned_data['last_name']
            parent.user.email = self.cleaned_data['email']
            parent.user.save()
            
        if commit:
            parent.save()
            
        return parent

class ParentListView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, ListView):
    model = ParentProfile
    template_name = 'parents/parent_list.html'
    context_object_name = 'parents'
    allowed_roles = ['Admin']
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('user')

class ParentDetailView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DetailView):
    model = ParentProfile
    template_name = 'parents/parent_detail.html'
    context_object_name = 'parent'
    allowed_roles = ['Admin']

class ParentCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = ParentProfile
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['Admin']

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class ParentUpdateView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, UpdateView):
    model = ParentProfile
    form_class = ParentForm
    template_name = 'parents/parent_form.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['Admin']

class ParentDeleteView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DeleteView):
    model = ParentProfile
    template_name = 'parents/parent_confirm_delete.html'
    success_url = reverse_lazy('parent_list')
    allowed_roles = ['Admin']
