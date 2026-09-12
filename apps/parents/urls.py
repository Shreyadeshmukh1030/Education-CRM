from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParentListView.as_view(), name='parent_list'),
    path('add/', views.ParentCreateView.as_view(), name='parent_add'),
]
