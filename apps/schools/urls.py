from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.SchoolSettingsUpdateView.as_view(), name='school_settings'),
]
