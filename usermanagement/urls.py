from django.urls import path
from .views import UserView, GroupView, FeedbackListCreateView

urlpatterns = [
    path('register/',UserView.as_view({'post':'register'}),name='register'),
    path('login/',UserView.as_view({'post':'login'}),name='login'),
    path('role/',GroupView.as_view({'get':'list'}),name='role-listing'), 
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
]