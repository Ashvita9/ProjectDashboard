from django.urls import path
from projectapp.views import ProjectView, TaskView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list-create'),
    path('tasks/', TaskView.as_view(), name='task-list-create'),
]
