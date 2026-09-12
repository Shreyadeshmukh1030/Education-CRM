from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='teacher_list'),
    path('add/', views.TeacherCreateView.as_view(), name='teacher_add'),
]
