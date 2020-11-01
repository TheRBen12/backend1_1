from typing import List
from rest_framework import serializers


def serializeList(list: List):
    return serializers.serialize('json', list);


class PersonSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField()
    size = serializers.FloatField()
    uploaded_at = serializers.DateField()
    public = serializers.BooleanField()
    price = serializers.FloatField
