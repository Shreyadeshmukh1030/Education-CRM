import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.accounts.models import User
from apps.academics.models import Class
from apps.teachers.models import TeacherProfile
from apps.students.models import StudentProfile
from apps.schools.models import School

try:
    user = User.objects.get(username='teacher')
    school = School.objects.first()
    
    teacher, created = TeacherProfile.objects.get_or_create(
        user=user,
        defaults={
            'school': school,
            'employee_id': 'T001', 
            'department': 'Science', 
            'joining_date': '2020-01-01'
        }
    )
    
    classes = Class.objects.all()
    teacher.classes.set(classes)
    teacher.save()
    
    # Also assign the test student to the first class so they show up
    student_user = User.objects.get(username='student')
    student, created = StudentProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'school': school,
            'student_id': 'S001', 
            'date_of_birth': '2010-05-15', 
            'blood_group': 'O+', 
            'gender': 'Male'
        }
    )
    student.current_class = classes.first()
    student.save()
    
    print("Assigned classes to teacher and student.")
except Exception as e:
    print(f"Error: {e}")
