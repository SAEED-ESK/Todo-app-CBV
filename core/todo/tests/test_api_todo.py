from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Todo

import pytest

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def common_user():
    user = User.objects.create(username='no_one', password='aA#12345')
    return user 

@pytest.fixture
def example_task(common_user):
    user = common_user
    user = Todo.objects.create(user=user, title='test')
    return user 

@pytest.mark.django_db
class TestApiTodo:
    def test_list_todo_response_401_status(self, api_client):
        url = reverse('todo:api/v1:todo-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_list_todo_response_200_status(self, api_client, common_user):
        url = reverse('todo:api/v1:todo-list')
        api_client.force_authenticate(user=common_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_todo_response_201_status(self, api_client, common_user):
        url = reverse('todo:api/v1:todo-list')
        data = {
            'title': 'test create'
        }
        api_client.force_authenticate(user=common_user)
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert response.data['title'] == 'test create'

    def test_detail_todo_response_200_status(self, api_client, common_user, example_task):
        api_client.force_authenticate(user=common_user)
        url = reverse('todo:api/v1:todo-detail', kwargs={'pk': example_task.id})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['title'] == 'test'


    def test_put_todo_response_200_status(self, api_client, common_user, example_task):
        api_client.force_authenticate(user=common_user)
        url = reverse('todo:api/v1:todo-detail', kwargs={'pk': example_task.id})
        data = {
            'title': 'test',
            'complete': True
        }
        response = api_client.put(url, data)
        assert response.status_code == 200
        assert response.data['complete'] == True

    def test_patch_todo_response_200_status(self, api_client, common_user, example_task):
        api_client.force_authenticate(user=common_user)
        url = reverse('todo:api/v1:todo-detail', kwargs={'pk': example_task.id})
        data = {
            'title': 'edited test'
        }
        response = api_client.patch(url, data)
        assert response.status_code == 200
        assert response.data['title'] == 'edited test'

    def test_delete_todo_response_204_status(self, api_client, common_user, example_task):
        api_client.force_authenticate(user=common_user)
        url = reverse('todo:api/v1:todo-detail', kwargs={'pk': example_task.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Todo.objects.filter(pk=example_task.id).exists() == False

        