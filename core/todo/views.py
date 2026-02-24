from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Todo


# Create your views here.
class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    login_url = "/accounts/login/"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title"]
    template_name = "todo/todo_list.html"
    success_url = reverse_lazy("todo:todo_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TodoEditView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title"]
    template_name = "todo/todo_edit.html"
    success_url = reverse_lazy("todo:todo_list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class TodoCompleteView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = []
    success_url = reverse_lazy("todo:todo_list")

    def form_valid(self, form):
        form.instance.complete = True
        return super().form_valid(form)
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
class TodoUndoView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = []
    success_url = reverse_lazy("todo:todo_list")

    def form_valid(self, form):
        form.instance.complete = False
        return super().form_valid(form)
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("todo:todo_list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)