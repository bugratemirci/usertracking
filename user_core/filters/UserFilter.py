from rest_framework import generics
from django_filters import rest_framework as filters
from ..models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'contains'],
        }
