from celery import shared_task
from .models import Todo

@shared_task
def delete_todo():
    Todo.objects.filter(complete=True).delete()
    print('Delete all complete todos')
