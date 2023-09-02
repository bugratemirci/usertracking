from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewset)
router.register(r'posts', views.PostViewset)
router.register(r'comments', views.CommentViewset)
router.register(r'todos', views.TodoViewset)
router.register(r'photos', views.PhotoViewset)
router.register(r'albums', views.AlbumViewset)


urlpatterns = [
    path('', include(router.urls)),
]
