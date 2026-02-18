from django.urls import path, include
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.TodoListView.as_view(), name="todo_list"),
    path(
        "complete/<int:pk>",
        views.TodoCompleteView.as_view(),
        name="todo_complete",
    ),
    path("edit/<int:pk>", views.TodoEditView.as_view(), name="todo_edit"),
    path("delete/<int:pk>", views.TodoDeleteView.as_view(), name="todo_delete"),
    path("create/", views.TodoCreateView.as_view(), name="todo_create"),
    path("api/v1/", include("todo.api.v1.urls")),
]
