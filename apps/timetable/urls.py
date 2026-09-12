from django.urls import path
from . import views

urlpatterns = [
    path('', views.TimetableView.as_view(), name='timetable_view'),
]
