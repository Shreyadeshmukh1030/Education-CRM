from django.db import models
from apps.schools.models import School

class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=50, help_text="e.g., 2026-2027")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('school', 'name')

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=50, help_text="e.g., Grade 10")
    order = models.IntegerField(default=0, help_text="Used for sorting classes")

    class Meta:
        unique_together = ('school', 'name')
        verbose_name_plural = 'Classes'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name}"

class Section(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10, help_text="e.g., A, B, C")
    
    class Meta:
        unique_together = ('school', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    classes = models.ManyToManyField(Class, related_name='subjects')
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class SyllabusTopic(models.Model):
    STATUS_CHOICES = (
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='syllabus_topics')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class StudyMaterial(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='materials')
    topic = models.ForeignKey(SyllabusTopic, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField()
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.assignment.title}"

class Announcement(models.Model):
    TYPE_CHOICES = (
        ('Test', 'Test'),
        ('Assignment', 'Assignment'),
        ('Event', 'Event'),
        ('Material', 'Material'),
        ('School Notice', 'School Notice'),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=TYPE_CHOICES, default='School Notice')
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements', help_text="Leave blank for school-wide")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Exam(models.Model):
    title = models.CharField(max_length=255)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.class_assigned.name}"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('exam', 'student')
    
    def __str__(self):
        return f"{self.student.user.first_name} - {self.exam.title}"
