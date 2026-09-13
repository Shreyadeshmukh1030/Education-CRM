from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.SchoolSettingsUpdateView.as_view(), name='school_settings'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcements'),
    path('updates/', views.SchoolUpdateListView.as_view(), name='school_updates'),
]
