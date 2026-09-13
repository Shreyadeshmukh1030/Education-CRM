from django.db import models
from apps.schools.models import School
from apps.academics.models import AcademicYear, Class
from apps.students.models import StudentProfile

class FeeCategory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class FeeStructure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date_rule = models.CharField(max_length=255, blank=True, help_text="e.g. 5th of every month")
    
    class Meta:
        unique_together = ('academic_year', 'class_assigned', 'category')
        
    def __str__(self):
        return f"{self.class_assigned.name} - {self.category.name} - {self.amount}"

class Invoice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='invoices')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='invoices')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.student}"

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Cheque', 'Cheque'),
        ('Online', 'Online'),
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"Payment {self.id} for {self.invoice.student}"
