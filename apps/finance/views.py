from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.mixins import RoleRequiredMixin, SchoolIsolationMixin
from .models import Invoice
from django import forms

class InvoiceListView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, ListView):
    model = Invoice
    template_name = 'students/fee_list.html'  # Reusing old template
    context_object_name = 'invoices'
    allowed_roles = ['Admin', 'Parent']
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if 'Admin' in user.role.name:
            return qs.select_related('student').order_by('-due_date')
        elif 'Parent' in user.role.name:
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(student__in=parent.children.all()).select_related('student').order_by('-due_date')
        return qs.none()

class InvoiceCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Invoice
    template_name = 'students/fee_form.html'
    fields = ['student', 'academic_year', 'title', 'amount', 'due_date', 'is_paid']
    success_url = reverse_lazy('fee_list')
    allowed_roles = ['Admin']

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class InvoiceUpdateView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, UpdateView):
    model = Invoice
    template_name = 'students/fee_form.html'
    fields = ['student', 'academic_year', 'title', 'amount', 'due_date', 'is_paid']
    success_url = reverse_lazy('fee_list')
    allowed_roles = ['Admin']

class InvoiceDeleteView(LoginRequiredMixin, RoleRequiredMixin, SchoolIsolationMixin, DeleteView):
    model = Invoice
    template_name = 'students/fee_confirm_delete.html'
    success_url = reverse_lazy('fee_list')
    allowed_roles = ['Admin']
