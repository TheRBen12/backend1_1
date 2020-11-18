from rest_framework import serializers


class PersonSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()
    id = serializers.IntegerField()


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField()
    uploaded_at = serializers.DateTimeField()
    public = serializers.BooleanField()
    price = serializers.FloatField


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    created_at = serializers.DateTimeField()


class InvitationSerializer(serializers.Serializer):
    sender = PersonSerializer()
    group = GroupSerializer()
    created_at = serializers.DateTimeField()
    creator = serializers.IntegerField()

class ShareFilePersonSerializer:
    file = serializers.FileField()













