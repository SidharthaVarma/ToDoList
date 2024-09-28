from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
# Create your views here.
# def home(request):
#     return HttpResponse("Working")

class TaskList(ListView):
    model= Task
    context_object_name = 'task'
    template_name = 'todo/task_list.html'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
    template_name='todo/task.html'