import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.accounts.models import User, Role
from apps.schools.models import School
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeacherProfile
from apps.parents.models import ParentProfile
from apps.academics.models import Class, Section, Subject, AcademicYear
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def run_seed():
    print("Seeding database...")
    
    # 1. School
    school, _ = School.objects.get_or_create(
        name="EduCore International School",
        defaults={
            "address": "123 Education Lane, Knowledge City",
            "phone": "555-0100",
            "email": "contact@educore.edu"
        }
    )
    print(f"School created: {school.name}")

    # 2. Roles
    admin_role, _ = Role.objects.get_or_create(name='Admin', description='System Administrator')
    teacher_role, _ = Role.objects.get_or_create(name='Teacher', description='School Teacher')
    student_role, _ = Role.objects.get_or_create(name='Student', description='School Student')
    parent_role, _ = Role.objects.get_or_create(name='Parent', description='Student Parent')
    
    # 3. Admin User
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
    if created:
        print("Admin user created (admin@educore.edu / admin123)")

    # 4. Academic Year
    year, _ = AcademicYear.objects.get_or_create(
        school=school,
        name="2024-2025",
        defaults={
            "start_date": "2024-04-01",
            "end_date": "2025-03-31",
            "is_active": True
        }
    )

    # 5. Classes & Sections
    classes = []
    for i in range(1, 13):
        cls, _ = Class.objects.get_or_create(school=school, name=f"Class {i}", order=i)
        classes.append(cls)
        
    sections = []
    for sec_name in ['A', 'B', 'C', 'D']:
        sec, _ = Section.objects.get_or_create(school=school, name=sec_name)
        sections.append(sec)

    # 6. Subjects
    subject_names = ['Mathematics', 'Science', 'English', 'History', 'Geography', 'Physics', 'Chemistry', 'Biology']
    subjects = []
    for idx, sub in enumerate(subject_names):
        subject, _ = Subject.objects.get_or_create(school=school, name=sub, code=sub[:3].upper())
        subject.classes.set(classes)
        subjects.append(subject)

    # 7. Teachers
    print("Creating teachers...")
    teachers = []
    for i in range(1, 41):
        email = f"teacher{i}@educore.edu"
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': f'Teacher{i}',
                'last_name': 'Staff',
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
        
    # 8. Parents & Students
    print("Creating parents and students (this may take a minute)...")
    
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    
    for i in range(1, 2001):
        if i % 100 == 0:
            print(f"  Created {i} students...")
            
        parent_email = f"parent{i}@example.com"
        parent_user, _ = User.objects.get_or_create(
            email=parent_email,
            defaults={
                'username': parent_email,
                'first_name': f'Parent{i}',
                'last_name': 'Family',
                'role': parent_role,
                'password': make_password('password123')
            }
        )
        parent, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            school=school,
            defaults={
                'occupation': 'Professional',
                'relationship_to_student': 'Father',
                'address': f"{random.randint(1, 999)} Main St, City"
            }
        )
        
        student_email = f"student{i}@educore.edu"
        student_user, _ = User.objects.get_or_create(
            email=student_email,
            defaults={
                'username': student_email,
                'first_name': f'Student{i}',
                'last_name': 'Family',
                'role': student_role,
                'password': make_password('password123')
            }
        )
        
        assigned_class = classes[(i % 12)]
        assigned_section = random.choice(sections)
        
        student, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            school=school,
            defaults={
                'student_id': f'S{20240000+i}',
                'date_of_birth': timezone.now().date() - timedelta(days=random.randint(3000, 6000)),
                'gender': random.choice(['Male', 'Female']),
                'blood_group': random.choice(blood_groups),
                'address': parent.address,
                'emergency_contact': f"555-01{i%100:02d}",
                'current_class': assigned_class
            }
        )
        
        # Link to parent
        parent.children.add(student)
        
        # Enrollment
        Enrollment.objects.get_or_create(
            student=student,
            academic_year=year,
            defaults={
                'student_class': assigned_class,
                'section': assigned_section,
                'roll_number': f"{i%40 + 1}"
            }
        )

    print("Seeding completed successfully!")

if __name__ == '__main__':
    run_seed()
