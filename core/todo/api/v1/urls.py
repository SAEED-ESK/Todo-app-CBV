from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api/v1'

router = DefaultRouter()
router.register('todo', views.TodoViewSet, basename='todo')

urlpatterns = router.urls
