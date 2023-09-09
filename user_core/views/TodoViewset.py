from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Todo, User
from ..serializers.TodoSerializer import TodoSerializer
from ..middleware.PaginationBackend import CustomPagination

from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema, no_body
from ..middleware.PaginationBackend import CustomPagination
from drf_yasg import openapi
from ..exception.BadRequestException import BadRequestException


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
        user_id = request.query_params.get('user_id', None)
        if user_id == None:
            raise BadRequestException("User id can't be null.")
        data = request.data

        data['user'] = user_id

        todo_serializer = self.get_serializer(data=data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY,
                              description="User ID", type=openapi.TYPE_STRING, required=True),
        ],
        request_body=no_body
    )
    @action(detail=False, methods=['GET'], url_path='gettodosbyuser')
    def get_todos_by_user(self, request):
        user_id = request.query_params.get('user_id', -1)
        if user_id == -1:
            raise BadRequestException("User id not found!")
        try:
            user = User.objects.get(id=user_id)
            todos = Todo.objects.filter(user=user)

            page = self.paginate_queryset(todos)
            data = TodoSerializer(page, many=True)

            return self.get_paginated_response(data.data)
        except Exception as e:
            raise BadRequestException("User or todo not found!")

    @action(detail=False, methods=['PUT'], url_path='settodotocomplete')
    def get_todos_by_user(self, request):
        todo_id = request.query_params.get('todo_id', None)
        if todo_id == None:
            raise BadRequestException("Todo id not found!")
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.completed = not todo.completed
            todo.save()

            data = TodoSerializer(todo)

            return Response(data.data)

        except Todo.DoesNotExist as e:
            raise BadRequestException(str(e))
        except Exception as e:
            raise BadRequestException(str(e))
