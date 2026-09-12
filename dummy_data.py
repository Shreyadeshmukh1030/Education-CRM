import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'educore.settings')
django.setup()

from apps.academics.models import Announcement, Exam, Subject, Class
from apps.schools.models import School, SchoolUpdate
from datetime import date, timedelta

school = School.objects.first()
subject = Subject.objects.first()
cls = Class.objects.first()
today = date.today()

if school and cls:
    SchoolUpdate.objects.create(school=school, title="School will remain closed on 25th April 2025", content="Holiday")
    SchoolUpdate.objects.create(school=school, title="Your meeting with parents is scheduled for tomorrow", content="Meeting")
    SchoolUpdate.objects.create(school=school, title="Fee reminder for few students in your class", content="Fees")

    if subject:
        Announcement.objects.create(title="Weekly Test - Science (Class 6-8)", content="The weekly test for Science will be conducted on...", category="Test", class_assigned=cls)
        Announcement.objects.create(title="Homework Reminder", content="Please submit the homework by tomorrow...", category="Assignment", class_assigned=cls)
        Announcement.objects.create(title="School Event - Annual Day", content="Annual Day celebration will be held on 25th April...", category="Event")
        Announcement.objects.create(title="New Study Material Added", content="Chapter 5 notes are now available in the study...", category="Material", class_assigned=cls)

        Exam.objects.create(title="Mid Term Exam", class_assigned=cls, subject=subject, date=today - timedelta(days=7))
        Exam.objects.create(title="Unit Test", class_assigned=cls, subject=subject, date=today - timedelta(days=12))
        Exam.objects.create(title="Monthly Test", class_assigned=cls, subject=subject, date=today - timedelta(days=17))
        
print("Dummy data added successfully.")
