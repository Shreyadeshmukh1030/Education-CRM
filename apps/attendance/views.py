from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.academics.models import Class
from apps.students.models import StudentProfile
from .models import AttendanceRecord
from datetime import date

class AttendanceSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance/attendance_select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # In a full app, we might filter classes based on the logged-in teacher
        context['classes'] = Class.objects.all()
        context['today'] = date.today().strftime('%Y-%m-%d')
        return context

class AttendanceMarkingView(LoginRequiredMixin, View):
    
    def get(self, request, class_id, date_str):
        class_obj = get_object_or_404(Class, id=class_id)
        # Assuming we just fetch all students in the school for now, 
        # normally we'd filter by student.current_class == class_obj
        students = StudentProfile.objects.filter(current_class=class_obj)
        
        # Check existing records
        existing_records = AttendanceRecord.objects.filter(
            class_assigned=class_obj, 
            date=date_str
        ).select_related('student')
        
        record_map = {r.student_id: r for r in existing_records}
        
        student_data = []
        for student in students:
            record = record_map.get(student.id)
            student_data.append({
                'student': student,
                'status': record.status if record else 'Present' # Default to Present
            })
            
        context = {
            'class_obj': class_obj,
            'date_str': date_str,
            'student_data': student_data,
        }
        return render(request, 'attendance/attendance_mark.html', context)
        
    def post(self, request, class_id, date_str):
        class_obj = get_object_or_404(Class, id=class_id)
        students = StudentProfile.objects.filter(current_class=class_obj)
        
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                # Update or create
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    date=date_str,
                    defaults={
                        'class_assigned': class_obj,
                        'status': status,
                        'marked_by': request.user
                    }
                )
        
        messages.success(request, f"Attendance saved for {class_obj.name} on {date_str}.")
        return redirect('attendance_select')
