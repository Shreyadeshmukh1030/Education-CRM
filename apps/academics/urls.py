from django.urls import path
from . import views

urlpatterns = [
    # Classes
    path('', views.ClassListView.as_view(), name='class_list'),
    path('add/', views.ClassCreateView.as_view(), name='class_add'),
    path('<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_edit'),
    path('<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),
    
    # Sections
    path('sections/', views.SectionListView.as_view(), name='section_list'),
    path('sections/add/', views.SectionCreateView.as_view(), name='section_add'),
    path('sections/<int:pk>/edit/', views.SectionUpdateView.as_view(), name='section_edit'),
    path('sections/<int:pk>/delete/', views.SectionDeleteView.as_view(), name='section_delete'),

    # Subjects
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),

    # Syllabus
    path('syllabus/', views.SyllabusListView.as_view(), name='syllabus_list'),
    path('syllabus/add/', views.SyllabusCreateView.as_view(), name='syllabus_add'),
    path('syllabus/<int:pk>/edit/', views.SyllabusUpdateView.as_view(), name='syllabus_edit'),
    path('syllabus/<int:pk>/delete/', views.SyllabusDeleteView.as_view(), name='syllabus_delete'),

    # Assignments
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/add/', views.AssignmentCreateView.as_view(), name='assignment_add'),
    path('assignments/<int:pk>/edit/', views.AssignmentUpdateView.as_view(), name='assignment_edit'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    
    # Assignment Submissions
    path('assignments/<int:assignment_id>/submit/', views.AssignmentSubmissionCreateView.as_view(), name='assignment_submit'),

    # Study Materials
    path('materials/', views.StudyMaterialListView.as_view(), name='material_list'),
    path('materials/add/', views.StudyMaterialCreateView.as_view(), name='material_add'),
    path('materials/<int:pk>/edit/', views.StudyMaterialUpdateView.as_view(), name='material_edit'),
    path('materials/<int:pk>/delete/', views.StudyMaterialDeleteView.as_view(), name='material_delete'),
    
    # Exams
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/add/', views.ExamCreateView.as_view(), name='exam_add'),
    path('exams/<int:pk>/edit/', views.ExamUpdateView.as_view(), name='exam_edit'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),
    path('exams/<int:exam_id>/results/', views.ExamResultMarkingView.as_view(), name='exam_results_mark'),
]
