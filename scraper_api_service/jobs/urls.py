from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListAPIView.as_view(), name='job-list'),
    path('<int:pk>/', views.JobDetailAPIView.as_view(), name='job-detail'),
]