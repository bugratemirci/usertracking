from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.UserViewset import UserViewset
from .views.PostViewset import PostViewset
from .views.CommentViewset import CommentViewset
from .views.TodoViewset import TodoViewset
from .views.AlbumViewset import AlbumViewset
from .views.PhotoViewset import PhotoViewset

router = DefaultRouter()
router.register(r'users', UserViewset)
router.register(r'posts', PostViewset)
router.register(r'comments', CommentViewset)
router.register(r'todos', TodoViewset)
router.register(r'photos', PhotoViewset)
router.register(r'albums', AlbumViewset)

urlpatterns = [
    path('', include(router.urls)),
]
