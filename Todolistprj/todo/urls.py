from django.urls import path
from .views import TaskList, TaskDetail

urlpatterns = [
    path('',TaskList.as_view(),name="task"),
    path('task/<int:pk>/',TaskDetail.as_view(),name="task-detail"), #here the int:pk is used to identify the task like url: .....task/3
]