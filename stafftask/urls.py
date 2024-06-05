from django.urls import path
from .views import StaffListCreateAPIView, StaffDetailAPIView, TaskListCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path('staff/', StaffListCreateAPIView.as_view(), name='staff-list-create'),
    path('staff/<int:pk>/', StaffDetailAPIView.as_view(), name='staff-detail'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
]
