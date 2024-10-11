from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
# def home(request):
#     return HttpResponse("Working")

class TaskList(LoginRequiredMixin,ListView):
    model= Task
    context_object_name = 'task'
    template_name = 'todo/task_list.html'

    def get_context_data(self,**kmargs):
        #this is used to filter the task list by the user
        context = super().get_context_data(**kmargs)
        context['task'] = context['task'].filter(user=self.request.user)
        context['count'] = context['task'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['task'] = context['task'].filter(title__icontains=search_input)
            context['search_input']=search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'task'
    template_name='todo/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    #fields = "__all__" #this is used to create a form with all the fields
    fields = ['title','description','complete']
    success_url= reverse_lazy('task') #this is used to redirect to the task list

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy('task')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task' 
    success_url = reverse_lazy('task')

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = False
    
    def get_success_url(self):
        return reverse_lazy('task')
    
class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    # this is used to redirect the user to the task list if he is already logged in and not allowing to the register page
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage, self).get(*args, **kwargs)