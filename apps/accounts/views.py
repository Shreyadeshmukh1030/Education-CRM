from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.students.models import StudentProfile
from apps.teachers.models import TeacherProfile
from apps.academics.models import Class
from apps.parents.models import ParentProfile

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
                    teacher_context = {
                        'teacher': teacher,
                        'total_assigned_students': 0, # To be implemented
                        'today_classes_count': 0,
                        'pending_assignments': 0,
                    }
                    return render(request, 'dashboard/teacher_dashboard.html', teacher_context)
                else:
                    return render(request, 'dashboard/teacher_dashboard.html', context)
            except Exception:
                return render(request, 'dashboard/teacher_dashboard.html', context)
        elif 'parent' in role_name:
            return render(request, 'dashboard/parent_dashboard.html', context)
        elif 'student' in role_name:
            return render(request, 'dashboard/student_dashboard.html', context)
            
    # Default to a generic dashboard or super admin
    return render(request, 'dashboard/admin_dashboard.html', context)
