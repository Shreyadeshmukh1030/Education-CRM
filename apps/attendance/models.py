from django.db import models

class AttendanceRecord(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    )
    
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='attendance_records')
    class_assigned = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    marked_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('student', 'date')
        
    def __str__(self):
        return f"{self.student.user.first_name} - {self.date} - {self.status}"
