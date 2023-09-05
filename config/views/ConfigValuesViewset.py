from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from ..models import ConfigValues
from ..serializers.ConfigValuesSerializer import ConfigValuesSerializer


class ConfigValuesViewset(ModelViewSet):
    queryset = ConfigValues.objects.all()
    serializer_class = ConfigValuesSerializer
