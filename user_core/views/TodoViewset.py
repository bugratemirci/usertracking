from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Todo, User
from ..serializers.TodoSerializer import TodoSerializer
from ..middleware.PaginationBackend import CustomPagination

from rest_framework.decorators import action


class TodoViewset(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    pagination_class = CustomPagination

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data

        data['user'] = user_id

        todo_serializer = self.get_serializer(data=data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)

    @action(detail=False, methods=['GET'], url_path='gettodosbyuser')
    def get_todos_by_user(self, request):
        user_id = request.query_params.get('user_id')
        user = User.objects.get(id=user_id)
        todos = Todo.objects.filter(user=user)
        page = self.paginate_queryset(todos)
        data = TodoSerializer(page, many=True)

        return self.get_paginated_response(data.data)
