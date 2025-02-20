from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Todo

# Create your views here.
class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    login_url = "/accounts/login/"
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class TodoCreateView(LoginRequiredMixin, CreateView, ListView):
    model = Todo
    fields = ['title']
    template_name = 'todo/todo_list.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TodoEditView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title']
    template_name = 'todo/todo_edit.html'
    success_url = '/'

class TodoCompleteView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = []
    template_name = 'todo/todo_list.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.complete = True
        return super().form_valid(form)
    
class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todo/todo_list.html'
    success_url = '/'
