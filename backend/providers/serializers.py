from rest_framework import serializers

from .models import ProviderAvailability, ProviderProfile


class ProviderProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = ProviderProfile
        fields = ["id", "email", "first_name", "last_name", "specialty", "bio", "created_at"]


class ProviderAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderAvailability
        fields = ["id", "date", "start_time", "end_time", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        start = data.get("start_time")
        end = data.get("end_time")
        if start and end and start >= end:
            raise serializers.ValidationError("start_time must be before end_time.")
        return data
