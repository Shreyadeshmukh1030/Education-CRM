from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttendanceSelectView.as_view(), name='attendance_select'),
    path('mark/<int:class_id>/<str:date_str>/', views.AttendanceMarkingView.as_view(), name='attendance_mark'),
    path('overview/<int:class_id>/<str:date_str>/', views.AttendanceOverviewView.as_view(), name='attendance_overview'),
]
