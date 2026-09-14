import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.accounts.models import User, Role
from apps.schools.models import School, SchoolUpdate
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeacherProfile
from apps.parents.models import ParentProfile
from apps.academics.models import Class, Section, Subject, AcademicYear, Exam, ExamResult, Announcement
from apps.finance.models import FeeCategory, FeeStructure, Invoice, Payment
from apps.attendance.models import AttendanceRecord
from apps.timetable.models import ClassSchedule, Period
from django.utils import timezone
from django.contrib.auth.hashers import make_password

INDIAN_FIRST_NAMES = [
    'Aarav', 'Vihaan', 'Vivaan', 'Ananya', 'Diya', 'Aditi', 'Advik', 'Kabir',
    'Tara', 'Myra', 'Aryan', 'Riya', 'Kavya', 'Saanvi', 'Ishaan', 'Arjun',
    'Neha', 'Rohan', 'Prisha', 'Krishna', 'Aanya', 'Pari', 'Siddharth', 'Aditya',
    'Rishi', 'Sneha', 'Meera', 'Karan', 'Vedant', 'Rahul', 'Nisha', 'Aisha',
    'Kiran', 'Amit', 'Pooja', 'Vikram', 'Shruti', 'Anjali', 'Kriti', 'Yash'
]

INDIAN_LAST_NAMES = [
    'Sharma', 'Patel', 'Singh', 'Kumar', 'Das', 'Reddy', 'Patil', 'Joshi',
    'Verma', 'Gupta', 'Mehta', 'Kulkarni', 'Deshmukh', 'Chauhan', 'Iyer',
    'Nair', 'Bhatt', 'Rajput', 'Rao', 'Kapoor', 'Malhotra', 'Bose', 'Chatterjee',
    'Banerjee', 'Ghosh', 'Sen', 'Mishra', 'Pandey', 'Tiwari', 'Yadav'
]

def run_seed():
    print("Clearing existing data (except core structure)...")
    StudentProfile.objects.all().delete()
    ParentProfile.objects.all().delete()
    User.objects.filter(role__name__in=['Student', 'Parent']).delete()
    ExamResult.objects.all().delete()
    Exam.objects.all().delete()
    Invoice.objects.all().delete()
    Payment.objects.all().delete()
    AttendanceRecord.objects.all().delete()
    Announcement.objects.all().delete()
    SchoolUpdate.objects.all().delete()
    ClassSchedule.objects.all().delete()

    print("Seeding database...")
    
    school, _ = School.objects.get_or_create(
        name="EduCore International School",
        defaults={
            "address": "123 Education Lane, Knowledge City",
            "phone": "555-0100",
            "email": "contact@educore.edu"
        }
    )
    print(f"School created: {school.name}")

    admin_role, _ = Role.objects.get_or_create(name='Admin', description='System Administrator')
    teacher_role, _ = Role.objects.get_or_create(name='Teacher', description='School Teacher')
    student_role, _ = Role.objects.get_or_create(name='Student', description='School Student')
    parent_role, _ = Role.objects.get_or_create(name='Parent', description='Student Parent')
    
    admin_user, created = User.objects.get_or_create(
        email='admin@educore.edu',
        defaults={
            'username': 'admin@educore.edu',
            'first_name': 'Super',
            'last_name': 'Admin',
            'role': admin_role,
            'is_staff': True,
            'is_superuser': True,
            'password': make_password('admin123')
        }
    )

    year, _ = AcademicYear.objects.get_or_create(
        school=school,
        name="2024-2025",
        defaults={
            "start_date": "2024-04-01",
            "end_date": "2025-03-31",
            "is_active": True
        }
    )

    classes = []
    for i in range(1, 13):
        cls, _ = Class.objects.get_or_create(school=school, name=f"Class {i}", order=i)
        classes.append(cls)
        
    sections = []
    for sec_name in ['A', 'B', 'C', 'D']:
        sec, _ = Section.objects.get_or_create(school=school, name=sec_name)
        sections.append(sec)

    subject_names = ['Mathematics', 'Science', 'English', 'History', 'Geography', 'Physics', 'Chemistry', 'Biology']
    subjects = []
    for idx, sub in enumerate(subject_names):
        subject, _ = Subject.objects.get_or_create(school=school, name=sub, code=sub[:3].upper())
        subject.classes.set(classes)
        subjects.append(subject)

    print("Creating teachers...")
    teachers = []
    for i in range(1, 21):
        f_name = random.choice(INDIAN_FIRST_NAMES)
        l_name = random.choice(INDIAN_LAST_NAMES)
        email = f"teacher{i}@educore.edu"
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': f_name,
                'last_name': l_name,
                'role': teacher_role,
                'password': make_password('password123')
            }
        )
        teacher, _ = TeacherProfile.objects.get_or_create(
            user=user,
            school=school,
            defaults={
                'employee_id': f'T{i:04d}',
                'department': random.choice(['Science', 'Arts', 'Math', 'English']),
                'joining_date': timezone.now().date() - timedelta(days=random.randint(100, 1000))
            }
        )
        if not teacher.classes.exists():
            teacher.classes.set(random.sample(classes, k=2))
        if not teacher.subjects.exists():
            teacher.subjects.set(random.sample(subjects, k=2))
        teachers.append(teacher)
        
    print("Creating timetable schedules...")
    periods = []
    times = [('08:00', '08:45'), ('09:00', '09:45'), ('10:00', '10:45'), ('11:00', '11:45'), ('12:30', '13:15')]
    for start, end in times:
        p, _ = Period.objects.get_or_create(school=school, start_time=start, end_time=end, defaults={'name': f"Period {start}"})
        periods.append(p)
        
    for cls in classes:
        for day in range(5):
            for period in periods:
                t = random.choice(teachers)
                sub = random.choice(subjects)
                ClassSchedule.objects.get_or_create(
                    school=school,
                    class_assigned=cls,
                    day_of_week=day,
                    period=period,
                    defaults={
                        'teacher': t,
                        'subject': sub,
                        'room': f"Room {random.randint(101, 205)}"
                    }
                )

    print("Creating Exams...")
    exams = []
    for cls in classes:
        for sub in random.sample(subjects, 3):
            exam, _ = Exam.objects.get_or_create(
                school=school,
                title=f"Mid-Term {sub.name}",
                class_assigned=cls,
                subject=sub,
                date=timezone.now().date() + timedelta(days=random.randint(1, 15))
            )
            exams.append(exam)

    print("Creating exactly 200 parents and students...")
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    students = []
    
    for i in range(1, 201):
        if i % 50 == 0:
            print(f"  Created {i} students...")
            
        p_first = random.choice(INDIAN_FIRST_NAMES)
        p_last = random.choice(INDIAN_LAST_NAMES)
        parent_email = f"parent{i}_{p_last.lower()}@example.com"
        parent_user, _ = User.objects.get_or_create(
            email=parent_email,
            defaults={
                'username': parent_email,
                'first_name': p_first,
                'last_name': p_last,
                'role': parent_role,
                'password': make_password('password123')
            }
        )
        parent, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            school=school,
            defaults={
                'occupation': random.choice(['Engineer', 'Doctor', 'Business', 'Teacher', 'Architect']),
                'relationship_to_student': random.choice(['Father', 'Mother']),
                'address': f"{random.randint(1, 999)} {random.choice(['Park Ave', 'Main St', 'Gandhi Road', 'Ring Road'])}"
            }
        )
        
        s_first = random.choice(INDIAN_FIRST_NAMES)
        student_email = f"student{i}_{s_first.lower()}@educore.edu"
        student_user, _ = User.objects.get_or_create(
            email=student_email,
            defaults={
                'username': student_email,
                'first_name': s_first,
                'last_name': p_last,
                'role': student_role,
                'password': make_password('password123')
            }
        )
        
        assigned_class = classes[(i % 12)]
        assigned_section = random.choice(sections)
        
        days_ago = random.randint(0, 180)
        admission_date = timezone.now().date() - timedelta(days=days_ago)

        student, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            school=school,
            defaults={
                'student_id': f'S{20240000+i}',
                'date_of_birth': timezone.now().date() - timedelta(days=random.randint(3000, 6000)),
                'gender': random.choice(['Male', 'Female']),
                'blood_group': random.choice(blood_groups),
                'address': parent.address,
                'emergency_contact': f"98{random.randint(10000000, 99999999)}",
                'current_class': assigned_class,
                'admission_date': admission_date
            }
        )
        students.append(student)
        
        parent.children.add(student)
        
        Enrollment.objects.get_or_create(
            student=student,
            academic_year=year,
            defaults={
                'student_class': assigned_class,
                'section': assigned_section,
                'roll_number': f"{i%40 + 1}"
            }
        )

        student_exams = [e for e in exams if e.class_assigned == assigned_class]
        for e in student_exams:
            ExamResult.objects.get_or_create(
                school=school,
                exam=e,
                student=student,
                defaults={
                    'marks_obtained': random.randint(45, 100)
                }
            )
            
        fee_amount = random.choice([15000, 20000, 25000, 30000])
        invoice, _ = Invoice.objects.get_or_create(
            school=school,
            student=student,
            academic_year=year,
            title="Term 1 Tuition Fee",
            defaults={
                'amount': fee_amount,
                'due_date': timezone.now().date() - timedelta(days=30),
                'is_paid': random.choice([True, False, False])
            }
        )
        if invoice.is_paid:
            Payment.objects.get_or_create(
                invoice=invoice,
                defaults={
                    'amount_paid': fee_amount,
                    'payment_method': random.choice(['Bank Transfer', 'Online', 'Cash'])
                }
            )

    print("Creating Attendance for last 7 days...")
    today = timezone.now().date()
    for day_offset in range(7):
        curr_date = today - timedelta(days=day_offset)
        if curr_date.weekday() >= 5: 
            continue
        for student in students:
            status = random.choices(['Present', 'Absent', 'Late', 'Excused'], weights=[85, 8, 5, 2])[0]
            AttendanceRecord.objects.get_or_create(
                student=student,
                date=curr_date,
                defaults={
                    'class_assigned': student.current_class,
                    'status': status
                }
            )

    print("Creating Announcements and Events...")
    for title, cat in [
        ("Term 1 Exams Rescheduled", "School Notice"),
        ("Annual Science Fair", "Event"),
        ("Holiday for Diwali", "School Notice")
    ]:
        Announcement.objects.get_or_create(
            school=school,
            title=title,
            defaults={
                'content': f"Details about {title}",
                'category': cat,
                'class_assigned': None,
                'created_at': timezone.now() - timedelta(days=random.randint(1, 10))
            }
        )
        
    for title in ["Sports Day Photos", "Science Fair Winners"]:
        SchoolUpdate.objects.get_or_create(
            school=school,
            title=title,
            defaults={
                'content': f"Highlights from {title}",
                'date': timezone.now().date() - timedelta(days=random.randint(1, 10))
            }
        )

    print("\n==================================")
    print("Seeding completed successfully!")
    print("Demo Login Credentials:")
    print("Admin:   admin@educore.edu / admin123")
    print("Teacher: teacher1@educore.edu / password123")
    print("Student: <see list> / password123")
    print("Parent:  <see list> / password123")
    print("==================================\n")

if __name__ == '__main__':
    run_seed()
