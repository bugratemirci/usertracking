from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import Todo
from ..serializers.TodoSerializer import TodoSerializer


class TodoViewset(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def create(self, request):
        user_id = request.query_params.get('user_id')
        data = request.data

        data['user'] = user_id

        todo_serializer = self.get_serializer(data=data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()
        return Response(todo_serializer.data)
