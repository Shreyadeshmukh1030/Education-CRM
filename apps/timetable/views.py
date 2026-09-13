from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ClassSchedule, Period
from apps.academics.models import Class
from apps.schools.models import School
from django import forms

class TimetableView(LoginRequiredMixin, TemplateView):
    template_name = 'timetable/timetable_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # We can pass a specific class if requested, default to the first class for demo
        class_id = self.request.GET.get('class_id')
        school = self.request.user.school
        if class_id:
            selected_class = Class.objects.filter(id=class_id, school=school).first()
        else:
            selected_class = Class.objects.filter(school=school).first()
            
        context['classes'] = Class.objects.filter(school=school)
        context['selected_class'] = selected_class
        
        if selected_class:
            periods = Period.objects.filter(school=school).order_by('order', 'start_time')
            schedules = ClassSchedule.objects.filter(class_assigned=selected_class, school=school).select_related('period', 'subject', 'teacher')
            
            # Map schedules for easy lookup in template: schedule_map[day][period_id] = schedule
            schedule_map = {}
            for day in [c[0] for c in ClassSchedule.DAY_CHOICES]:
                schedule_map[day] = {}
                
            for schedule in schedules:
                schedule_map[schedule.day_of_week][schedule.period_id] = schedule
                
            context['periods'] = periods
            context['schedule_map'] = schedule_map
            context['days'] = [c[0] for c in ClassSchedule.DAY_CHOICES]
            
        return context

# --- PERIODS ---
class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'start_time', 'end_time', 'is_break', 'order']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PeriodListView(LoginRequiredMixin, ListView):
    model = Period
    template_name = 'timetable/period_list.html'
    context_object_name = 'periods'

class PeriodCreateView(LoginRequiredMixin, CreateView):
    model = Period
    form_class = PeriodForm
    template_name = 'timetable/period_form.html'
    success_url = reverse_lazy('period_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class PeriodUpdateView(LoginRequiredMixin, UpdateView):
    model = Period
    form_class = PeriodForm
    template_name = 'timetable/period_form.html'
    success_url = reverse_lazy('period_list')

class PeriodDeleteView(LoginRequiredMixin, DeleteView):
    model = Period
    template_name = 'timetable/period_confirm_delete.html'
    success_url = reverse_lazy('period_list')


# --- CLASS SCHEDULES ---
class ClassScheduleListView(LoginRequiredMixin, ListView):
    model = ClassSchedule
    template_name = 'timetable/schedule_list.html'
    context_object_name = 'schedules'

class ClassScheduleCreateView(LoginRequiredMixin, CreateView):
    model = ClassSchedule
    template_name = 'timetable/schedule_form.html'
    fields = ['class_assigned', 'period', 'day_of_week', 'subject', 'teacher', 'room']
    success_url = reverse_lazy('schedule_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class ClassScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = ClassSchedule
    template_name = 'timetable/schedule_form.html'
    fields = ['class_assigned', 'period', 'day_of_week', 'subject', 'teacher', 'room']
    success_url = reverse_lazy('schedule_list')

class ClassScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = ClassSchedule
    template_name = 'timetable/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_list')

