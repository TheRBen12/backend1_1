from rest_framework import serializers


class PersonSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()
    id = serializers.IntegerField()


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()
    name = serializers.CharField()
    size = serializers.FloatField()
    uploaded_at = serializers.DateField()
    public = serializers.BooleanField()
    price = serializers.FloatField


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField()
    created_at = serializers.DateField()
    creator = serializers.IntegerField()


class InvitationSerializer(serializers.Serializer):
    sender = PersonSerializer()
    group = GroupSerializer()
    created_at = serializers.DateField()
    creator = serializers.IntegerField()







