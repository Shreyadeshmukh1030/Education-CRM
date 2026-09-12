"""
URL configuration for educore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.accounts.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('students/', include('apps.students.urls')),
    path('teachers/', include('apps.teachers.urls')),
    path('classes/', include('apps.academics.urls')),
    path('parents/', include('apps.parents.urls')),
    path('school/', include('apps.schools.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('timetable/', include('apps.timetable.urls')),
    
    # Placeholders for unbuilt modules
    path('announcements/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='announcements'),
    path('examinations/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='examinations'),
    path('results/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='results'),
    path('attendance-reports/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='attendance_reports'),
    path('syllabus/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='syllabus'),
    path('fees/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='fees'),
    path('messages/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='messages_app'),
    path('school-updates/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='school_updates'),
    path('reminders/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='reminders'),
    path('my-profile/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='my_profile'),
    path('my-settings/', auth_views.TemplateView.as_view(template_name='pages/under_construction.html'), name='my_settings'),
    
    path('', dashboard_view, name='dashboard'),
]
