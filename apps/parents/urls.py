from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParentListView.as_view(), name='parent_list'),
    path('<int:pk>/', views.ParentDetailView.as_view(), name='parent_detail'),
    path('add/', views.ParentCreateView.as_view(), name='parent_add'),
    path('<int:pk>/edit/', views.ParentUpdateView.as_view(), name='parent_edit'),
    path('<int:pk>/delete/', views.ParentDeleteView.as_view(), name='parent_delete'),
]
