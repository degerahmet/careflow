from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    session_id = serializers.UUIDField(required=False, allow_null=True)
    message    = serializers.CharField(max_length=2000)


class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    reply      = serializers.CharField()
    step       = serializers.CharField()
    data       = serializers.DictField()
