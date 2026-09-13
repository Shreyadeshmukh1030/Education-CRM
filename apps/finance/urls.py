from django.urls import path
from . import views

urlpatterns = [
    path('', views.InvoiceListView.as_view(), name='fee_list'),
    path('add/', views.InvoiceCreateView.as_view(), name='fee_add'),
    path('<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='fee_edit'),
    path('<int:pk>/delete/', views.InvoiceDeleteView.as_view(), name='fee_delete'),
]
