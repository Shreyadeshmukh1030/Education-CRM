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
        classes = Class.objects.all()
        context['classes'] = classes
        context['today'] = date.today().strftime('%Y-%m-%d')
        
        # Check if user is admin
        is_admin = False
        if getattr(self.request.user, 'role', None) and self.request.user.role.name.lower() == 'admin':
            is_admin = True
        context['is_admin'] = is_admin
        
        # Check counselor status for teacher
        counselor_classes = []
        if hasattr(self.request.user, 'teacher_profile'):
            counselor_class = getattr(self.request.user.teacher_profile, 'counselor_for_class', None)
            if counselor_class:
                counselor_classes.append(counselor_class.id)
        
        context['counselor_classes'] = counselor_classes
        
        return context

class AttendanceMarkingView(LoginRequiredMixin, View):
    
    def get(self, request, class_id, date_str):
        if getattr(request.user, 'role', None) and request.user.role.name.lower() == 'admin':
            messages.error(request, "Admins cannot mark attendance. Please view the dashboard reports.")
            return redirect('attendance_select')
            
        class_obj = get_object_or_404(Class, id=class_id)
        
        # Counselor Check
        if hasattr(request.user, 'teacher_profile'):
            if getattr(class_obj, 'counselor', None) != request.user.teacher_profile:
                messages.error(request, "Permission denied: Only the Class Counselor can mark attendance.")
                return redirect('attendance_select')
        
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
        if getattr(request.user, 'role', None) and request.user.role.name.lower() == 'admin':
            messages.error(request, "Admins cannot mark attendance.")
            return redirect('attendance_select')
            
        class_obj = get_object_or_404(Class, id=class_id)
        
        # Counselor Check
        if hasattr(request.user, 'teacher_profile'):
            if getattr(class_obj, 'counselor', None) != request.user.teacher_profile:
                messages.error(request, "Permission denied: Only the Class Counselor can mark attendance.")
                return redirect('attendance_select')
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

class AttendanceOverviewView(LoginRequiredMixin, View):
    def get(self, request, class_id, date_str):
        # Admins or any teacher can view this
        class_obj = get_object_or_404(Class, id=class_id)
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
                'status': record.status if record else 'Not Marked'
            })
            
        context = {
            'class_obj': class_obj,
            'date_str': date_str,
            'student_data': student_data,
        }
        return render(request, 'attendance/attendance_overview.html', context)
