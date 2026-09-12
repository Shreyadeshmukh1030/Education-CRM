from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClassListView.as_view(), name='class_list'),
    path('add/', views.ClassCreateView.as_view(), name='class_add'),
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/add/', views.AssignmentCreateView.as_view(), name='assignment_add'),
    path('materials/', views.StudyMaterialListView.as_view(), name='material_list'),
    path('materials/add/', views.StudyMaterialCreateView.as_view(), name='material_add'),
]
