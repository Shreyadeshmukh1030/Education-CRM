import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.accounts.models import User
from apps.students.models import StudentProfile, FeeInvoice
from apps.academics.models import Exam, ExamResult, Assignment, AssignmentSubmission, Subject, Class
from apps.timetable.models import ClassSchedule, Period

def create_student_data():
    try:
        user = User.objects.get(username='student')
        student = StudentProfile.objects.get(user=user)
        current_class = student.current_class
        school = student.school
        
        if not current_class:
            current_class = Class.objects.first()
            student.current_class = current_class
            student.save()
            
        print(f"Adding data for {student} in {current_class}")
        today = date.today()
        
        # Add Fee Invoices
        FeeInvoice.objects.get_or_create(student=student, title="Term 1 Tuition Fee", defaults={'amount': 12000, 'due_date': today + timedelta(days=30), 'is_paid': False})
        FeeInvoice.objects.get_or_create(student=student, title="Library Fee", defaults={'amount': 500, 'due_date': today - timedelta(days=10), 'is_paid': True})
        
        # Add Exam Results
        exams = Exam.objects.filter(class_assigned=current_class)[:4]
        scores = [85, 78, 82, 75]
        for idx, exam in enumerate(exams):
            ExamResult.objects.get_or_create(student=student, exam=exam, defaults={'marks_obtained': scores[idx]})
            
        # Add Timetable if none
        if not ClassSchedule.objects.filter(class_assigned=current_class, day_of_week=today.weekday()).exists():
            periods = Period.objects.filter(school=school).order_by('start_time')[:6]
            subjects = Subject.objects.filter(classes=current_class)[:6]
            teacher = current_class.assigned_teachers.first()
            
            for idx, period in enumerate(periods):
                if idx < len(subjects) and teacher:
                    ClassSchedule.objects.get_or_create(
                        class_assigned=current_class,
                        period=period,
                        day_of_week=today.weekday(),
                        defaults={
                            'subject': subjects[idx],
                            'teacher': teacher
                        }
                    )
        
        print("Student dummy data created successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_student_data()
