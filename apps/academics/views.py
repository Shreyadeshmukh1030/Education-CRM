from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Class, Section, Subject, SyllabusTopic, Assignment, StudyMaterial, AssignmentSubmission, Exam, ExamResult
from apps.students.models import StudentProfile
from apps.schools.models import School
from apps.accounts.mixins import SchoolIsolationMixin
from django import forms

# --- CLASSES ---
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'order']

    def save(self, commit=True):
        if commit:
            class_instance.save()
        return class_instance

class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'academics/class_list.html'
    context_object_name = 'classes'

class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'academics/class_form.html'
    success_url = reverse_lazy('class_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = 'academics/class_form.html'
    success_url = reverse_lazy('class_list')

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = Class
    template_name = 'academics/class_confirm_delete.html'
    success_url = reverse_lazy('class_list')

# --- SECTIONS ---
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        
    def save(self, commit=True):
        if commit:
            section_instance.save()
        return section_instance

class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = 'academics/section_list.html'
    context_object_name = 'sections'

class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/section_form.html'
    success_url = reverse_lazy('section_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class SectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'academics/section_form.html'
    success_url = reverse_lazy('section_list')

class SectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Section
    template_name = 'academics/section_confirm_delete.html'
    success_url = reverse_lazy('section_list')

# --- SUBJECTS ---
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'classes']
        widgets = {
            'classes': forms.CheckboxSelectMultiple()
        }
        
    def save(self, commit=True):
        if commit:
            subject_instance.save()
            self.save_m2m()
        return subject_instance

class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('subject_list')

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    template_name = 'academics/subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

# --- SYLLABUS ---
class SyllabusListView(LoginRequiredMixin, ListView):
    model = SyllabusTopic
    template_name = 'academics/syllabus_list.html'
    context_object_name = 'topics'

class SyllabusCreateView(LoginRequiredMixin, CreateView):
    model = SyllabusTopic
    template_name = 'academics/syllabus_form.html'
    fields = ['subject', 'class_assigned', 'name', 'description', 'status']
    success_url = reverse_lazy('syllabus_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class SyllabusUpdateView(LoginRequiredMixin, UpdateView):
    model = SyllabusTopic
    template_name = 'academics/syllabus_form.html'
    fields = ['subject', 'class_assigned', 'name', 'description', 'status']
    success_url = reverse_lazy('syllabus_list')

class SyllabusDeleteView(LoginRequiredMixin, DeleteView):
    model = SyllabusTopic
    template_name = 'academics/syllabus_confirm_delete.html'
    success_url = reverse_lazy('syllabus_list')


# --- ASSIGNMENTS ---
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'academics/assignment_list.html'
    context_object_name = 'assignments'
    ordering = ['-due_date']

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = Assignment
    template_name = 'academics/assignment_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'due_date', 'max_marks', 'attachment']
    success_url = reverse_lazy('assignment_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class AssignmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assignment
    template_name = 'academics/assignment_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'due_date', 'max_marks', 'attachment']
    success_url = reverse_lazy('assignment_list')

class AssignmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'academics/assignment_confirm_delete.html'
    success_url = reverse_lazy('assignment_list')

class AssignmentSubmissionCreateView(LoginRequiredMixin, CreateView):
    model = AssignmentSubmission
    template_name = 'academics/assignment_submit.html'
    fields = ['file']
    
    def get_success_url(self):
        return reverse('assignment_list')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(Assignment, id=self.kwargs['assignment_id'])
        return context
        
    def form_valid(self, form):
        form.instance.assignment = get_object_or_404(Assignment, id=self.kwargs['assignment_id'])
        form.instance.school = self.request.user.school
        # Assuming request.user is a student
        form.instance.student = getattr(self.request.user, 'student_profile', None)
        return super().form_valid(form)

# --- STUDY MATERIALS ---
class StudyMaterialListView(LoginRequiredMixin, ListView):
    model = StudyMaterial
    template_name = 'academics/material_list.html'
    context_object_name = 'materials'
    ordering = ['-uploaded_at']

class StudyMaterialCreateView(LoginRequiredMixin, CreateView):
    model = StudyMaterial
    template_name = 'academics/material_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'topic', 'file']
    success_url = reverse_lazy('material_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class StudyMaterialUpdateView(LoginRequiredMixin, UpdateView):
    model = StudyMaterial
    template_name = 'academics/material_form.html'
    fields = ['title', 'description', 'subject', 'class_assigned', 'topic', 'file']
    success_url = reverse_lazy('material_list')

class StudyMaterialDeleteView(LoginRequiredMixin, DeleteView):
    model = StudyMaterial
    template_name = 'academics/material_confirm_delete.html'
    success_url = reverse_lazy('material_list')

# --- EXAMS ---
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'class_assigned', 'subject', 'date', 'max_marks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'academics/exam_list.html'
    context_object_name = 'exams'
    ordering = ['-date']

class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'academics/exam_form.html'
    success_url = reverse_lazy('exam_list')

    def form_valid(self, form):
        form.instance.school = self.request.user.school
        return super().form_valid(form)

class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'academics/exam_form.html'
    success_url = reverse_lazy('exam_list')

class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'academics/exam_confirm_delete.html'
    success_url = reverse_lazy('exam_list')

class ExamResultMarkingView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        students = StudentProfile.objects.filter(current_class=exam.class_assigned)
        
        # Check existing results
        existing_results = ExamResult.objects.filter(exam=exam).select_related('student')
        result_map = {r.student_id: r for r in existing_results}
        
        student_data = []
        for student in students:
            result = result_map.get(student.id)
            student_data.append({
                'student': student,
                'marks': result.marks_obtained if result else ''
            })
            
        context = {
            'exam': exam,
            'student_data': student_data,
        }
        return render(request, 'academics/exam_results_mark.html', context)
        
    def post(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        students = StudentProfile.objects.filter(current_class=exam.class_assigned)
        
        for student in students:
            marks = request.POST.get(f'marks_{student.id}')
            if marks is not None and marks.strip() != '':
                ExamResult.objects.update_or_create(
                    exam=exam,
                    student=student,
                    defaults={'marks_obtained': float(marks)}
                )
        
        messages.success(request, f"Results saved for {exam.title}.")
        return redirect('exam_list')
