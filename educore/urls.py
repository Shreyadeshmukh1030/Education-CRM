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
from apps.accounts.views import dashboard_view, landing_page_view

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
    path('fees/', include('apps.finance.urls')),
    
    
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', landing_page_view, name='landing'),
]
