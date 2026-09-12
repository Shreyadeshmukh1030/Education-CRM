import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.accounts.models import User, Role
from apps.teachers.models import TeacherProfile
from apps.students.models import StudentProfile
from apps.parents.models import ParentProfile
from apps.schools.models import School

def create_test_users():
    print("Creating test users...")
    
    # Ensure School exists
    school, _ = School.objects.get_or_create(
        name="EduCore Demo School",
        defaults={'email': 'contact@educore.test', 'phone': '1234567890'}
    )
    
    # Define roles
    roles = ['Admin', 'Teacher', 'Student', 'Parent']
    role_objs = {}
    for r in roles:
        role_objs[r], _ = Role.objects.get_or_create(name=r)
        
    users_created = []

    # 1. Admin
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.role = role_objs['Admin']
        admin_user.first_name = "Super"
        admin_user.last_name = "Admin"
        admin_user.save()
        users_created.append("admin:admin123 (Admin)")

    # 2. Teacher
    teacher_user, created = User.objects.get_or_create(username='teacher')
    if created:
        teacher_user.set_password('teacher123')
        teacher_user.role = role_objs['Teacher']
        teacher_user.first_name = "Jane"
        teacher_user.last_name = "Smith"
        teacher_user.save()
        
        TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={
                'school': school,
                'employee_id': 'T001', 
                'department': 'Science', 
                'joining_date': '2020-01-01'
            }
        )
        users_created.append("teacher:teacher123 (Teacher)")

    # 3. Student
    student_user, created = User.objects.get_or_create(username='student')
    if created:
        student_user.set_password('student123')
        student_user.role = role_objs['Student']
        student_user.first_name = "John"
        student_user.last_name = "Doe"
        student_user.save()
        
        StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'school': school,
                'student_id': 'S001', 
                'date_of_birth': '2010-05-15', 
                'blood_group': 'O+', 
                'gender': 'Male'
            }
        )
        users_created.append("student:student123 (Student)")

    # 4. Parent
    parent_user, created = User.objects.get_or_create(username='parent')
    if created:
        parent_user.set_password('parent123')
        parent_user.role = role_objs['Parent']
        parent_user.first_name = "Robert"
        parent_user.last_name = "Doe"
        parent_user.save()
        
        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            defaults={
                'school': school,
                'occupation': 'Engineer'
            }
        )
        
        # Link student to parent
        sp = StudentProfile.objects.get(user=student_user)
        sp.parents.add(parent_profile)
        
        users_created.append("parent:parent123 (Parent)")
        
    print("Test users ready:")
    for u in users_created:
        print(f" - {u}")
    if not users_created:
        print("Users already exist.")

if __name__ == '__main__':
    create_test_users()
