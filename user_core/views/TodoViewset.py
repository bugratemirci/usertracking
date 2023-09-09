from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi

from ..models import Todo
from ..serializers.TodoSerializer import TodoSerializer
from ..middleware.PaginationBackend import CustomPagination
from ..service.TodoService import TodoService


class TodoViewset(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
        ]
    )
    def create(self, request):
        return Response(TodoService(request=request).create())

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
        ],
        request_body=no_body
    )
    @action(detail=False, methods=['GET'], url_path='gettodosbyuser')
    def get_todos_by_user(self, request):
        return TodoService(request=request).getTodosByUser(self.paginate_queryset, self.get_paginated_response)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('todo_id', openapi.IN_QUERY,
                              description="Todo ID", type=openapi.TYPE_STRING, required=True),
        ],
        request_body=no_body
    )
    @action(detail=False, methods=['PUT'], url_path='settodotocomplete')
    def set_todo_to_complete(self, request):
        return Response(TodoService(request=request).setTodoToComplete())
