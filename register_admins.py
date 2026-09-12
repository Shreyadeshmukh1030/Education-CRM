import os

apps_models = {
    'academics': ['AcademicYear', 'Class', 'Section'],
    'students': ['StudentProfile', 'Enrollment'],
    'parents': ['ParentProfile'],
    'teachers': ['TeacherProfile'],
}

for app, models in apps_models.items():
    admin_file = f'apps/{app}/admin.py'
    if os.path.exists(admin_file):
        with open(admin_file, 'w') as f:
            f.write('from django.contrib import admin\n')
            f.write(f'from .models import {", ".join(models)}\n\n')
            for model in models:
                f.write(f'admin.site.register({model})\n')
