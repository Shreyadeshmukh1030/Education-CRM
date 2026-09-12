from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.students.models import StudentProfile
from apps.teachers.models import TeacherProfile
from apps.academics.models import Class, Assignment, StudyMaterial, Announcement, Exam
from apps.parents.models import ParentProfile
from apps.timetable.models import ClassSchedule
from apps.attendance.models import AttendanceRecord
from apps.schools.models import SchoolUpdate
from datetime import date
from django.db.models import Count, Q

@login_required
def dashboard_view(request):
    user = request.user
    
    # Calculate stats
    total_students = StudentProfile.objects.count()
    total_teachers = TeacherProfile.objects.count()
    total_classes = Class.objects.count()
    total_parents = ParentProfile.objects.count()
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_parents': total_parents,
    }
    
    # Placeholder for role-based dashboard rendering
    if getattr(user, 'role', None):
        role_name = user.role.name.lower()
        if 'admin' in role_name:
            return render(request, 'dashboard/admin_dashboard.html', context)
        elif 'teacher' in role_name:
            # For teacher, get specific stats
            try:
                teacher = getattr(user, 'teacher_profile', None)
                if teacher:
                    today = date.today()
                    
                    # 1. Total Classes Assigned
                    assigned_classes = teacher.classes.all()
                    total_classes_assigned = assigned_classes.count()
                    
                    # 2. Total Students in those classes
                    total_assigned_students = StudentProfile.objects.filter(current_class__in=assigned_classes).count()
                    
                    # 3. Pending Assignments
                    pending_assignments = Assignment.objects.filter(class_assigned__in=assigned_classes, due_date__gte=today).count()
                    
                    # 4. Today's Attendance summary
                    attendance_today = AttendanceRecord.objects.filter(
                        student__current_class__in=assigned_classes, 
                        date=today
                    )
                    total_present = attendance_today.filter(status='Present').count()
                    total_absent = attendance_today.filter(status='Absent').count()
                    total_late = attendance_today.filter(status='Late').count()
                    total_marked = attendance_today.count()
                    attendance_percentage = int((total_present / total_marked * 100)) if total_marked > 0 else 0
                    
                    # 5. Class-wise Student Overview
                    class_overview = []
                    for c in assigned_classes:
                        students_count = StudentProfile.objects.filter(current_class=c).count()
                        class_attendance = AttendanceRecord.objects.filter(student__current_class=c, date=today)
                        c_present = class_attendance.filter(status='Present').count()
                        c_absent = class_attendance.filter(status='Absent').count()
                        c_marked = class_attendance.count()
                        c_perc = int((c_present / c_marked * 100)) if c_marked > 0 else 100
                        class_overview.append({
                            'class_obj': c,
                            'students_count': students_count,
                            'present': c_present,
                            'absent': c_absent,
                            'percentage': c_perc
                        })
                    
                    # 6. Upcoming Classes (Schedule)
                    # We assume day_of_week is stored as an integer (0-6) where 0 is Monday.
                    current_day = today.weekday()
                    upcoming_classes = ClassSchedule.objects.filter(
                        teacher=teacher, 
                        day_of_week=current_day
                    ).order_by('period__start_time')[:3]
                    
                    # 7. Recent Announcements
                    recent_announcements = Announcement.objects.filter(
                        Q(class_assigned__isnull=True) | Q(class_assigned__in=assigned_classes)
                    ).order_by('-created_at')[:4]
                    
                    # 8. Study Material
                    recent_materials = StudyMaterial.objects.filter(class_assigned__in=assigned_classes).order_by('-uploaded_at')[:3]
                    
                    # 9. Examinations
                    recent_exams = Exam.objects.filter(class_assigned__in=assigned_classes).order_by('-created_at')[:3]
                    
                    # 10. School Updates
                    school_updates = SchoolUpdate.objects.order_by('-date')[:3]

                    teacher_context = {
                        'teacher': teacher,
                        'total_classes_assigned': total_classes_assigned,
                        'total_assigned_students': total_assigned_students,
                        'pending_assignments': pending_assignments,
                        'attendance_percentage': attendance_percentage,
                        'total_present': total_present,
                        'total_absent': total_absent,
                        'total_late': total_late,
                        'total_marked': total_marked,
                        'class_overview': class_overview,
                        'upcoming_classes': upcoming_classes,
                        'recent_announcements': recent_announcements,
                        'recent_materials': recent_materials,
                        'recent_exams': recent_exams,
                        'school_updates': school_updates,
                        'today': today,
                    }
                    return render(request, 'dashboard/teacher_dashboard.html', teacher_context)
                else:
                    return render(request, 'dashboard/teacher_dashboard.html', context)
            except Exception as e:
                print("Dashboard error:", e)
                return render(request, 'dashboard/teacher_dashboard.html', context)
        elif 'parent' in role_name:
            return render(request, 'dashboard/parent_dashboard.html', context)
        elif 'student' in role_name:
            return render(request, 'dashboard/student_dashboard.html', context)
            
    # Default to a generic dashboard or super admin
    return render(request, 'dashboard/admin_dashboard.html', context)
