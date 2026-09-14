import pandas as pd
import random
import string
import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone
from apps.accounts.models import User, Role
from apps.schools.models import School
from apps.students.models import StudentProfile, Enrollment
from apps.parents.models import ParentProfile
from apps.academics.models import Class, Section, Subject, Exam, ExamResult
from apps.attendance.models import AttendanceRecord
from apps.finance.models import Invoice

class Command(BaseCommand):
    help = "Import Student and Parent data from Excel and replace existing data."

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def generate_random_password(self):
        return 'password123'

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        try:
            self.stdout.write("Reading Excel file...")
            df = pd.read_excel(file_path, sheet_name='Students Master Data')
        except Exception as e:
            self.stderr.write(f"Error reading Excel file: {e}")
            return
        
        with transaction.atomic():
            self.stdout.write("Deleting existing Student and Parent records...")
            User.objects.filter(role__name__in=['Student', 'Parent']).delete()
            self.stdout.write("Old data wiped successfully.")

            school = School.objects.first()
            if not school:
                self.stderr.write("No school found in the database. Please run seed_educore_demo first.")
                return

            student_role = Role.objects.get(name='Student')
            parent_role = Role.objects.get(name='Parent')

            # Dictionary to cache subjects by name to avoid query in loop
            subject_cache = {sub.name: sub for sub in Subject.objects.all()}
            
            # Map column names in excel to DB subjects
            subject_col_mapping = {
                'Mid-Sem - English (%)': 'English',
                'Mid-Sem - Mathematics (%)': 'Mathematics',
                'Mid-Sem - Science (%)': 'Science',
                'Mid-Sem - Social Science (%)': 'Social Science',
                'Mid-Sem - Hindi (%)': 'Hindi',
                'Mid-Sem - Computer Science (%)': 'Computer Science',
                'Mid-Sem - Physical Education (%)': 'Physical Education',
                'Mid-Sem - Physics (%)': 'Physics',
                'Mid-Sem - Chemistry (%)': 'Chemistry',
                'Mid-Sem - Biology (%)': 'Biology',
                'Mid-Sem - Information Technology (%)': 'Information Technology',
            }

            self.stdout.write("Importing data...")
            for index, row in df.iterrows():
                try:
                    # Parse Parent
                    father_email = str(row.get('Father Email', '')).strip()
                    if pd.isna(row.get('Father Email')) or not father_email or father_email.lower() == 'nan':
                        father_email = f"parent{index}@demo.com"
                        
                    parent_user = User.objects.create(
                        username=father_email,
                        email=father_email,
                        password=make_password(self.generate_random_password()),
                        role=parent_role,
                        school=school,
                        first_name=str(row.get('Father Name', 'Parent')).split(' ')[0],
                        last_name=' '.join(str(row.get('Father Name', 'Parent')).split(' ')[1:]) if ' ' in str(row.get('Father Name', '')) else ''
                    )
                    parent_profile = ParentProfile.objects.create(
                        user=parent_user,
                        school=school,
                        occupation=row.get('Father Occupation'),
                        relationship_to_student='Father',
                        address=row.get('Address')
                    )

                    # Parse Student
                    student_email = str(row.get('Student Email', '')).strip()
                    if pd.isna(row.get('Student Email')) or not student_email or student_email.lower() == 'nan':
                        student_email = f"student{index}@demo.com"

                    student_user = User.objects.create(
                        username=student_email,
                        email=student_email,
                        password=make_password(self.generate_random_password()),
                        role=student_role,
                        school=school,
                        first_name=str(row.get('Student Name', 'Student')).split(' ')[0],
                        last_name=' '.join(str(row.get('Student Name', 'Student')).split(' ')[1:]) if ' ' in str(row.get('Student Name', '')) else ''
                    )

                    dob = row.get('Date of Birth')
                    if pd.isna(dob):
                        dob = timezone.now().date() - datetime.timedelta(days=15*365)
                    elif isinstance(dob, datetime.datetime):
                        dob = dob.date()
                    elif isinstance(dob, str):
                        try:
                            dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
                        except:
                            dob = timezone.now().date() - datetime.timedelta(days=15*365)

                    student_profile = StudentProfile.objects.create(
                        user=student_user,
                        school=school,
                        student_id=row.get('Student ID'),
                        admission_date=timezone.now().date(),
                        date_of_birth=dob,
                        gender=row.get('Gender', 'Male'),
                        blood_group=row.get('Blood Group', 'O+'),
                        address=row.get('Address'),
                        emergency_contact=row.get('Emergency Contact Phone', '')
                    )

                    # Add child to parent (M2M)
                    student_profile.parents.add(parent_profile)

                    # Enrollment
                    class_num = row.get('Class')
                    if pd.isna(class_num):
                        continue
                    
                    class_obj = Class.objects.filter(school=school, name__contains=str(int(class_num))).first()
                    if not class_obj:
                        continue # Or create it, but we assume seed_educore_demo created them
                    
                    section_name = str(row.get('Section', 'A')).strip()
                    section_obj, _ = Section.objects.get_or_create(school=school, name=section_name)

                    from apps.academics.models import AcademicYear
                    ac_year_str = str(row.get('Academic Year', '2026-27')).strip()
                    ac_year_obj, _ = AcademicYear.objects.get_or_create(school=school, name=ac_year_str, defaults={
                        'start_date': timezone.now().date() - datetime.timedelta(days=100),
                        'end_date': timezone.now().date() + datetime.timedelta(days=265),
                        'is_active': True
                    })

                    Enrollment.objects.create(
                        student=student_profile,
                        student_class=class_obj,
                        section=section_obj,
                        roll_number=row.get('Roll No'),
                        academic_year=ac_year_obj
                    )
                    
                    # Update current class in profile for quick access
                    student_profile.current_class = class_obj
                    student_profile.current_section = section_obj
                    student_profile.save()

                    # Attendance Generation
                    attendance_pct = row.get('Attendance %')
                    if pd.notna(attendance_pct):
                        # Generate records for last 30 days based on %
                        total_days = 30
                        present_days = int((float(attendance_pct) / 100) * total_days)
                        
                        today = timezone.now().date()
                        days_list = [today - datetime.timedelta(days=i) for i in range(total_days)]
                        
                        # Randomize present days
                        random.shuffle(days_list)
                        present_dates = days_list[:present_days]
                        absent_dates = days_list[present_days:]
                        
                        attendance_records = []
                        for d in present_dates:
                            attendance_records.append(AttendanceRecord(
                                student=student_profile,
                                class_assigned=class_obj,
                                date=d,
                                status='Present'
                            ))
                        for d in absent_dates:
                            attendance_records.append(AttendanceRecord(
                                student=student_profile,
                                class_assigned=class_obj,
                                date=d,
                                status='Absent'
                            ))
                        AttendanceRecord.objects.bulk_create(attendance_records)

                    # Financial Invoices
                    overall_fee = row.get('Overall Fees (₹)')
                    paid_fee = row.get('Paid Fees (₹)')
                    pending_fee = row.get('Pending Fees (₹)')
                    
                    if pd.notna(overall_fee):
                        invoice = Invoice.objects.create(
                            school=school,
                            student=student_profile,
                            academic_year=ac_year_obj,
                            title="Annual Fee",
                            amount=Decimal(str(overall_fee)),
                            due_date=timezone.now().date() + datetime.timedelta(days=30),
                            is_paid=False if pd.notna(pending_fee) and pending_fee > 0 else True
                        )
                        if pd.notna(paid_fee) and paid_fee > 0:
                            from apps.finance.models import Payment
                            Payment.objects.create(
                                invoice=invoice,
                                amount_paid=Decimal(str(paid_fee)),
                                payment_method='Bank Transfer'
                            )

                    # Exam Results
                    for col, subj_name in subject_col_mapping.items():
                        marks = row.get(col)
                        if pd.notna(marks) and str(marks).lower() != 'nan':
                            # Ensure subject exists
                            subject_obj = subject_cache.get(subj_name)
                            if not subject_obj:
                                subject_obj, _ = Subject.objects.get_or_create(school=school, name=subj_name)
                                subject_cache[subj_name] = subject_obj
                                
                            # Ensure class assignment
                            if class_obj not in subject_obj.classes.all():
                                subject_obj.classes.add(class_obj)
                                
                            marks = float(marks)
                            
                            # Create class-subject specific Exam
                            exam_obj, _ = Exam.objects.get_or_create(
                                school=school,
                                title="Mid-Term Examination",
                                class_assigned=class_obj,
                                subject=subject_obj,
                                defaults={'date': timezone.now().date() - datetime.timedelta(days=20)}
                            )
                            
                            ExamResult.objects.create(
                                school=school,
                                exam=exam_obj,
                                student=student_profile,
                                marks_obtained=marks
                            )

                except Exception as e:
                    self.stderr.write(f"Error importing row {index} (Student: {row.get('Student Name')}): {e}")

            self.stdout.write(self.style.SUCCESS("Excel data imported successfully! Analytics will now reflect this data."))
