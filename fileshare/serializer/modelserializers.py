from abc import ABC

from rest_framework import serializers


class PersonSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()
    id = serializers.IntegerField()

class FileTypeSerializer(serializers.Serializer):
    type = serializers.CharField()

class FileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = FileTypeSerializer()
    file = serializers.FileField()
    name = serializers.CharField()
    uploaded_at = serializers.DateTimeField()
    price = serializers.FloatField()
    size = serializers.IntegerField()
    public = serializers.BooleanField()
    owner = PersonSerializer()

class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    created_at = serializers.DateTimeField()


class InvitationSerializer(serializers.Serializer):
    sender = PersonSerializer()
    group = GroupSerializer()
    created_at = serializers.DateTimeField()
    creator = serializers.IntegerField()


class ShareFilePersonSerializer(serializers.Serializer):
    file = FileSerializer()
    receiver = PersonSerializer()
    creator = PersonSerializer()
    shared_at = serializers.DateField()
