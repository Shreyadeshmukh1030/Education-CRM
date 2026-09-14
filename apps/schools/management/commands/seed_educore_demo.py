import os
import random
import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from apps.accounts.models import Role
from apps.schools.models import School
from apps.academics.models import AcademicYear, Class, Section, Subject, SyllabusTopic, StudyMaterial, Assignment, Exam, ExamResult, Announcement
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeacherProfile
from apps.parents.models import ParentProfile
from apps.attendance.models import AttendanceRecord
from apps.timetable.models import Period, ClassSchedule
from apps.finance.models import FeeCategory, FeeStructure, Invoice, Payment

User = get_user_model()
fake = Faker('en_IN')

class Command(BaseCommand):
    help = 'Seeds the EduCore database with exactly 135 students, 7 teachers, and complete ERP data.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Wiping existing demo data (excluding roles)...")
        
        # We don't wipe Roles. We wipe School and cascade everything to ensure a clean slate.
        School.objects.all().delete()
        # Also clean users except superusers
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write("Creating School and Basic Configuration...")
        school = School.objects.create(
            name="EduCore International School",
            address="123 Education Lane, Mumbai",
            phone="9876543210",
            email="info@educore.edu"
        )
        
        academic_year = AcademicYear.objects.create(
            school=school,
            name="2026-2027",
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2027, 3, 31),
            is_active=True
        )

        admin_role, _ = Role.objects.get_or_create(name='Admin')
        teacher_role, _ = Role.objects.get_or_create(name='Teacher')
        student_role, _ = Role.objects.get_or_create(name='Student')
        parent_role, _ = Role.objects.get_or_create(name='Parent')

        # Admin user
        admin_user = User.objects.create_user(
            username='admin@educore.edu', email='admin@educore.edu', password='admin123',
            first_name='Admin', last_name='User', role=admin_role, school=school
        )

        # Classes & Sections
        self.stdout.write("Creating Classes and Sections...")
        class_10 = Class.objects.create(school=school, name='Class 10', order=10)
        class_11 = Class.objects.create(school=school, name='Class 11', order=11)
        class_12 = Class.objects.create(school=school, name='Class 12', order=12)
        
        section_a = Section.objects.create(school=school, name='A')

        # Subjects
        self.stdout.write("Creating Subjects...")
        sub_eng = Subject.objects.create(school=school, name='English', code='ENG')
        sub_math = Subject.objects.create(school=school, name='Mathematics', code='MAT')
        sub_phy = Subject.objects.create(school=school, name='Physics', code='PHY')
        sub_che = Subject.objects.create(school=school, name='Chemistry', code='CHE')
        sub_bio = Subject.objects.create(school=school, name='Biology', code='BIO')
        sub_sst = Subject.objects.create(school=school, name='Social Science', code='SST')
        sub_cs = Subject.objects.create(school=school, name='Computer Science', code='CS')
        sub_it = Subject.objects.create(school=school, name='Information Technology', code='IT')

        for c in [class_10, class_11, class_12]:
            sub_eng.classes.add(c)
            sub_math.classes.add(c)
            sub_phy.classes.add(c)
            sub_che.classes.add(c)
            sub_bio.classes.add(c)
            sub_sst.classes.add(c)
            sub_cs.classes.add(c)
            if c in [class_11, class_12]:
                sub_it.classes.add(c)

        # Teachers
        self.stdout.write("Creating Teachers & Counselors...")
        teacher_names = [
            ("Priya", "Sharma"),
            ("Neha", "Kulkarni"),
            ("Snehal", "Patil"),
            ("Amit", "Joshi"),
            ("Rahul", "Deshmukh"),
            ("Pooja", "Verma"),
            ("Rohan", "Mehta"),
        ]

        teachers = []
        for i, (first, last) in enumerate(teacher_names, 1):
            email = f"teacher{i}@educore.edu"
            t_user = User.objects.create_user(
                username=email, email=email, password='password123',
                first_name=first, last_name=last, role=teacher_role, school=school
            )
            tp = TeacherProfile.objects.create(
                user=t_user, school=school, employee_id=f"EMP-T{i:03d}",
                department="Science" if i in [2,3,5] else "General",
                joining_date=datetime.date(2020 + (i%4), 6, 1)
            )
            teachers.append(tp)

        # Counselors
        teachers[0].counselor_for_class = class_10; teachers[0].save()
        teachers[1].counselor_for_class = class_11; teachers[1].save()
        teachers[2].counselor_for_class = class_12; teachers[2].save()

        # Teacher Subject assignments (realistic)
        teachers[0].subjects.add(sub_math); teachers[0].classes.add(class_10, class_11)
        teachers[1].subjects.add(sub_phy); teachers[1].classes.add(class_11, class_12)
        teachers[2].subjects.add(sub_che); teachers[2].classes.add(class_12, class_10)
        teachers[3].subjects.add(sub_eng); teachers[3].classes.add(class_10, class_11, class_12)
        teachers[4].subjects.add(sub_bio); teachers[4].classes.add(class_10, class_11, class_12)
        teachers[5].subjects.add(sub_cs); teachers[5].classes.add(class_10, class_11, class_12)
        teachers[6].subjects.add(sub_it, sub_sst); teachers[6].classes.add(class_10, class_11, class_12)

        # Periods & Timetable
        self.stdout.write("Creating Timetable...")
        periods = []
        start_t = datetime.datetime.strptime('08:00', '%H:%M')
        for i in range(1, 7):
            end_t = start_t + datetime.timedelta(minutes=45)
            periods.append(Period.objects.create(
                school=school, name=f"Period {i}",
                start_time=start_t.time(), end_time=end_t.time(), order=i
            ))
            start_t = end_t
            if i == 3:
                # Lunch
                end_t = start_t + datetime.timedelta(minutes=30)
                Period.objects.create(school=school, name="Lunch Break", start_time=start_t.time(), end_time=end_t.time(), is_break=True, order=i+0.5)
                start_t = end_t

        days = [0, 1, 2, 3, 4] # Mon-Fri
        for c in [class_10, class_11, class_12]:
            class_subs = list(c.subjects.all())
            for d in days:
                for p in periods:
                    sub = random.choice(class_subs)
                    t = sub.assigned_teachers.first()
                    if not t: t = random.choice(teachers)
                    ClassSchedule.objects.create(
                        school=school, class_assigned=c, period=p, day_of_week=d, subject=sub, teacher=t, room=f"Room {c.order}01"
                    )

        # 135 Students
        self.stdout.write("Creating exactly 135 Students & Parents...")
        classes_map = [class_10, class_11, class_12]
        student_id_counter = 1
        
        students = []
        for cl in classes_map:
            for r in range(1, 46): # 45 students per class
                parent_email = f"parent_{cl.order}_{r}@example.com"
                p_user = User.objects.create_user(
                    username=parent_email, email=parent_email, password='password123',
                    first_name=fake.first_name_male(), last_name=fake.last_name(), role=parent_role, school=school
                )
                parent = ParentProfile.objects.create(
                    user=p_user, school=school,
                    address=fake.address()
                )
                
                s_first = fake.first_name()
                s_last = p_user.last_name
                s_email = f"student_{cl.order}_{r}@educore.edu"
                
                s_user = User.objects.create_user(
                    username=s_email, email=s_email, password='password123',
                    first_name=s_first, last_name=s_last, role=student_role, school=school
                )
                
                st = StudentProfile.objects.create(
                    user=s_user, school=school, student_id=f"STU-{student_id_counter:04d}",
                    date_of_birth=fake.date_of_birth(minimum_age=14, maximum_age=18),
                    gender=random.choice(['Male', 'Female']),
                    blood_group=random.choice(['A+', 'B+', 'O+', 'AB+']),
                    admission_date=datetime.date(2023, 4, 1),
                    address=parent.address,
                    emergency_contact=fake.phone_number()[:15],
                    current_class=cl
                )
                st.parents.add(parent)
                
                Enrollment.objects.create(
                    student=st, academic_year=academic_year, student_class=cl, section=section_a,
                    roll_number=str(r), status='Active'
                )
                
                students.append(st)
                student_id_counter += 1

        # Exams & Marks
        self.stdout.write("Creating Exams and Results...")
        for cl in classes_map:
            for sub in cl.subjects.all():
                exam = Exam.objects.create(
                    school=school, title="Mid-Term Examination", class_assigned=cl,
                    subject=sub, date=datetime.date.today() - datetime.timedelta(days=15),
                    max_marks=100
                )
                
                # Results
                for s in students:
                    if s.current_class == cl:
                        ExamResult.objects.create(
                            school=school, exam=exam, student=s,
                            marks_obtained=Decimal(random.randint(40, 98))
                        )
                        
        # Fees
        self.stdout.write("Creating Fee Records...")
        fc = FeeCategory.objects.create(school=school, name='Tuition Fee')
        fs = FeeStructure.objects.create(school=school, class_assigned=class_10, academic_year=academic_year, category=fc, amount=Decimal('50000'))
        for s in students:
            inv = Invoice.objects.create(school=school, student=s, academic_year=academic_year, title=f"Term 1 {fc.name}", amount=fs.amount, due_date=datetime.date(2026,5,1), is_paid=False)
            
            # Pay some
            if random.random() > 0.3:
                Payment.objects.create(invoice=inv, amount_paid=fs.amount, payment_method='Bank Transfer')
                inv.is_paid = True
                inv.save()
                
        # Attendance
        self.stdout.write("Creating Attendance for last 7 days...")
        for i in range(7):
            d = datetime.date.today() - datetime.timedelta(days=i)
            if d.weekday() > 4: continue # Skip weekends
            
            for s in students:
                AttendanceRecord.objects.create(
                    student=s, class_assigned=s.current_class,
                    date=d, status=random.choices(['Present', 'Absent', 'Late'], weights=[90, 8, 2])[0],
                    marked_by=s.current_class.counselor.user if getattr(s.current_class, 'counselor', None) else admin_user
                )
                
        # Announcements
        self.stdout.write("Creating Announcements...")
        Announcement.objects.create(school=school, title="Mid-Term Examination Timetable Released", content="Please check the portal.", category='School Notice')
        Announcement.objects.create(school=school, title="Parent-Teacher Meeting", content="Scheduled for next week.", category='Event')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))
