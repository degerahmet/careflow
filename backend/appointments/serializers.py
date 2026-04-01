from rest_framework import serializers

from providers.models import ProviderAvailability
from providers.serializers import ProviderProfileSerializer

from .models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "provider", "scheduled_at", "reason"]

    def validate(self, data):
        provider = data.get("provider")
        scheduled_at = data.get("scheduled_at")

        if provider and scheduled_at:
            slot_date = scheduled_at.date()
            slot_time = scheduled_at.time()

            is_available = ProviderAvailability.objects.filter(
                provider=provider,
                date=slot_date,
                start_time__lte=slot_time,
                end_time__gt=slot_time,
            ).exists()

            if not is_available:
                raise serializers.ValidationError(
                    {"scheduled_at": "The provider has no availability at the requested time."}
                )

        return data

    def create(self, validated_data):
        validated_data["member"] = self.context["request"].user
        return super().create(validated_data)


class AppointmentReadSerializer(serializers.ModelSerializer):
    provider = ProviderProfileSerializer(read_only=True)
    member_email = serializers.EmailField(source="member.email", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "member_email",
            "provider",
            "scheduled_at",
            "reason",
            "status",
            "ai_summary",
            "created_at",
            "updated_at",
        ]


class AppointmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["status"]
