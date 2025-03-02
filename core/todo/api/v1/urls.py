from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('todo', views.TodoViewSet, basename='todo-list')

urlpatterns = router.urls
