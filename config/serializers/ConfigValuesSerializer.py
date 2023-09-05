from rest_framework import serializers
from ..models import ConfigValues


class ConfigValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigValues
        fields = ('key', 'value')
