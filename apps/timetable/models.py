from django.db import models

class Period(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='periods')
    name = models.CharField(max_length=50, help_text="e.g., Period 1, Lunch Break")
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'start_time']
        
    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

class ClassSchedule(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE, related_name='class_schedules')
    class_assigned = models.ForeignKey('academics.Class', on_delete=models.CASCADE, related_name='schedules')
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey('teachers.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules')
    room = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ('class_assigned', 'period', 'day_of_week')
        
    def __str__(self):
        return f"{self.class_assigned.name} - {self.get_day_of_week_display()} - {self.period.name}"
