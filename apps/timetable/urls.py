from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimetableView.as_view(), name='timetable_view'),
    
    # Periods
    path('periods/', views.PeriodListView.as_view(), name='period_list'),
    path('periods/add/', views.PeriodCreateView.as_view(), name='period_add'),
    path('periods/<int:pk>/edit/', views.PeriodUpdateView.as_view(), name='period_edit'),
    path('periods/<int:pk>/delete/', views.PeriodDeleteView.as_view(), name='period_delete'),

    # Schedules
    path('schedules/', views.ClassScheduleListView.as_view(), name='schedule_list'),
    path('schedules/add/', views.ClassScheduleCreateView.as_view(), name='schedule_add'),
    path('schedules/<int:pk>/edit/', views.ClassScheduleUpdateView.as_view(), name='schedule_edit'),
    path('schedules/<int:pk>/delete/', views.ClassScheduleDeleteView.as_view(), name='schedule_delete'),
]
