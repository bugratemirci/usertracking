from ..models import Todo, User
from ..serializers.TodoSerializer import TodoSerializer
from ..exception.BadRequestException import BadRequestException


class TodoService:
    def __init__(self, request) -> None:
        self.request = request

    def create(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id == None:
            raise BadRequestException("User id can't be null.")
        data = self.request.data

        data['user'] = user_id

        todo_serializer = TodoSerializer(data=data)
        todo_serializer.is_valid(raise_exception=True)
        todo_serializer.save()

        return todo_serializer.data

    def getTodosByUser(self, paginate_queryset, paginated_response):
        user_id = self.request.query_params.get('user_id', None)
        if user_id == None:
            raise BadRequestException("User id not found!")
        try:
            user = User.objects.get(id=user_id)
        except Exception as e:
            raise BadRequestException("User not found!")
        
        todos = Todo.objects.filter(user=user)
        page = paginate_queryset(todos)
        data = TodoSerializer(page, many=True)

        return paginated_response(data.data)

    def setTodoToComplete(self):
        todo_id = self.request.query_params.get('todo_id', None)
        if todo_id == None:
            raise BadRequestException("Todo id not found!")
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.completed = not todo.completed
            todo.save()

            serializer = TodoSerializer(todo)

            return serializer.data

        except Todo.DoesNotExist as e:
            raise BadRequestException(str(e))
        except Exception as e:
            raise BadRequestException(str(e))
