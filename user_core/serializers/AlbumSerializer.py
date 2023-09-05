from rest_framework import serializers
from ..models import Photo, Album
from .PhotoSerializer import PhotoSerializer


class AlbumSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = '__all__'

    def get_photos(self, obj):
        try:
            photo = Photo.objects.filter(album=obj)
            serializer = PhotoSerializer(photo, many=True)
            return serializer.data
        except Photo.DoesNotExist:
            return None
