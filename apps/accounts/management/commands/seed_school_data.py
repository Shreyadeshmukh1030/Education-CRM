import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import Role
from apps.schools.models import School
from apps.academics.models import AcademicYear, Class, Section, Subject
from apps.teachers.models import TeacherProfile
from apps.parents.models import ParentProfile
from apps.students.models import StudentProfile, Enrollment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with a realistic K-12 school structure and dummy data.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. Create Roles
        roles_data = ['Admin', 'Teacher', 'Student', 'Parent']
        roles = {}
        for r_name in roles_data:
            role, created = Role.objects.get_or_create(name=r_name)
            roles[r_name] = role
        self.stdout.write("Roles created.")

        # 2. Create School
        school, _ = School.objects.get_or_create(
            name="Bright Future School",
            defaults={
                'address': '123 Education Lane',
                'city': 'Metropolis',
                'state': 'State',
                'country': 'India',
                'phone': '+91 9876543210',
                'email': 'info@brightfuture.edu',
                'principal_name': 'Dr. Sarah Connor',
                'primary_color': '#4F46E5',
            }
        )
        self.stdout.write("School created.")

        # 3. Create Academic Year
        current_year = date.today().year
        ay, _ = AcademicYear.objects.get_or_create(
            school=school,
            name=f"{current_year}-{current_year+1}",
            defaults={
                'start_date': date(current_year, 4, 1),
                'end_date': date(current_year+1, 3, 31),
                'is_active': True
            }
        )
        self.stdout.write("Academic Year created.")

        # 4. Create Classes and Sections
        classes_data = [
            ("Nursery", 0), ("LKG", 1), ("UKG", 2),
            ("Class 1", 3), ("Class 2", 4), ("Class 3", 5),
            ("Class 4", 6), ("Class 5", 7), ("Class 6", 8),
            ("Class 7", 9), ("Class 8", 10), ("Class 9", 11),
            ("Class 10", 12), ("Class 11", 13), ("Class 12", 14)
        ]
        sections_data = ['A', 'B', 'C']
        
        created_classes = []
        for c_name, order in classes_data:
            c, _ = Class.objects.get_or_create(school=school, name=c_name, defaults={'order': order})
            created_classes.append(c)
            
        created_sections = []
        for s_name in sections_data:
            s, _ = Section.objects.get_or_create(school=school, name=s_name)
            created_sections.append(s)
            
        self.stdout.write("Classes and Sections created.")

        # 5. Create Subjects
        subjects_data = [
            ("Mathematics", "MATH"), ("Science", "SCI"), ("English", "ENG"), 
            ("Hindi", "HIN"), ("Social Studies", "SST"), ("Computer Science", "CS"),
            ("Physics", "PHY"), ("Chemistry", "CHEM"), ("Biology", "BIO")
        ]
        created_subjects = []
        for s_name, code in subjects_data:
            subj, _ = Subject.objects.get_or_create(name=s_name, school=school, defaults={'code': code})
            # Assign to some classes (e.g., all from Class 1 to 10)
            if s_name in ["Physics", "Chemistry", "Biology"]:
                subj.classes.set(Class.objects.filter(order__gte=13)) # Class 11 and 12
            else:
                subj.classes.set(Class.objects.filter(order__lte=12, order__gte=3)) # Class 1 to 10
            created_subjects.append(subj)
            
        self.stdout.write("Subjects created.")

        # 6. Create Users (Admin)
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@school.com', 'admin123')
            admin_user.role = roles['Admin']
            admin_user.school = school
            admin_user.first_name = "Super"
            admin_user.last_name = "Admin"
            admin_user.save()
            self.stdout.write("Admin user created (admin / admin123).")

        # 7. Create Teachers
        teacher_names = [
            ("Amit", "Sharma"), ("Priya", "Singh"), ("Rajesh", "Kumar"),
            ("Sneha", "Patel"), ("Vikram", "Reddy"), ("Anjali", "Desai")
        ]
        created_teachers = []
        for i, (fname, lname) in enumerate(teacher_names):
            username = f"teacher{i+1}"
            if not User.objects.filter(username=username).exists():
                t_user = User.objects.create_user(username=username, password='password123', email=f"{username}@school.com")
                t_user.first_name = fname
                t_user.last_name = lname
                t_user.role = roles['Teacher']
                t_user.school = school
                t_user.save()
                
                t_profile = TeacherProfile.objects.create(
                    user=t_user, school=school, employee_id=f"EMP{1000+i}", department="General"
                )
                # Assign some random classes and subjects
                t_profile.classes.set(random.sample(created_classes, 3))
                t_profile.subjects.set(random.sample(created_subjects, 2))
                created_teachers.append(t_profile)
        
        self.stdout.write(f"{len(created_teachers)} Teachers created (teacher1..N / password123).")

        # 8. Create Parents and Students
        # Generate 50 students
        student_first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Ayaan", "Krishna", "Ishaan", "Shaurya", "Diya", "Aanya", "Myra", "Ananya", "Kavya", "Pari"]
        student_last_names = ["Gupta", "Jain", "Mehta", "Bose", "Verma", "Rao", "Nair", "Iyer"]
        
        created_students = 0
        for i in range(1, 51):
            s_fname = random.choice(student_first_names)
            s_lname = random.choice(student_last_names)
            username = f"student{i}"
            
            if not User.objects.filter(username=username).exists():
                # Create Student User
                s_user = User.objects.create_user(username=username, password='password123', email=f"{username}@school.com")
                s_user.first_name = s_fname
                s_user.last_name = s_lname
                s_user.role = roles['Student']
                s_user.school = school
                s_user.save()
                
                # Pick a random class
                s_class = random.choice(created_classes)
                
                # Create Student Profile
                s_profile = StudentProfile.objects.create(
                    user=s_user, school=school, student_id=f"STU2024{i:03d}",
                    current_class=s_class, gender=random.choice(["Male", "Female"]),
                    admission_date=date(2023, 4, 1)
                )
                
                # Create Enrollment
                s_section = random.choice(created_sections)
                Enrollment.objects.create(
                    student=s_profile, academic_year=ay,
                    student_class=s_class, section=s_section,
                    roll_number=str(random.randint(1, 40))
                )
                
                # Create Parent (1 per student for simplicity)
                p_username = f"parent{i}"
                p_user = User.objects.create_user(username=p_username, password='password123', email=f"{p_username}@school.com")
                p_user.first_name = f"{s_fname}'s"
                p_user.last_name = "Parent"
                p_user.role = roles['Parent']
                p_user.school = school
                p_user.save()
                
                p_profile = ParentProfile.objects.create(
                    user=p_user, school=school, relationship_to_student="Father/Mother"
                )
                s_profile.parents.add(p_profile)
                created_students += 1

        self.stdout.write(f"{created_students} Students and Parents created.")
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
