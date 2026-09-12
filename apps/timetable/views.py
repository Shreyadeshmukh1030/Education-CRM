from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ClassSchedule, Period
from apps.academics.models import Class

class TimetableView(LoginRequiredMixin, TemplateView):
    template_name = 'timetable/timetable_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # We can pass a specific class if requested, default to the first class for demo
        class_id = self.request.GET.get('class_id')
        if class_id:
            selected_class = Class.objects.filter(id=class_id).first()
        else:
            selected_class = Class.objects.first()
            
        context['classes'] = Class.objects.all()
        context['selected_class'] = selected_class
        
        if selected_class:
            periods = Period.objects.all().order_by('order', 'start_time')
            schedules = ClassSchedule.objects.filter(class_assigned=selected_class).select_related('period', 'subject', 'teacher')
            
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
