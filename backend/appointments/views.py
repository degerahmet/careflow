from datetime import timedelta

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from providers.models import ProviderAvailability
from providers.permissions import IsMember, IsProvider

from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentReadSerializer,
    AppointmentStatusSerializer,
)


class AppointmentViewSet(CreateModelMixin, GenericViewSet):
    queryset = Appointment.objects.select_related("member", "provider__user").all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return AppointmentCreateSerializer
        if self.action == "update_status":
            return AppointmentStatusSerializer
        return AppointmentReadSerializer

    def get_permissions(self):
        if self.action in ("create", "member_list"):
            return [IsMember()]
        if self.action in ("provider_list", "update_status"):
            return [IsProvider()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path="member")
    def member_list(self, request):
        queryset = (
            Appointment.objects.filter(member=request.user)
            .select_related("member", "provider__user")
            .order_by("-scheduled_at")
        )
        serializer = AppointmentReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="provider")
    def provider_list(self, request):
        queryset = (
            Appointment.objects.filter(provider__user=request.user)
            .select_related("member", "provider__user")
            .order_by("-scheduled_at")
        )
        serializer = AppointmentReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        appointment = self.get_object()

        if appointment.provider.user != request.user:
            return Response(
                {"detail": "You do not have permission to update this appointment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AppointmentStatusSerializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data.get("status")
        serializer.save()

        # When a provider confirms an appointment, consume the overlapping availability slot.
        if new_status == Appointment.Status.CONFIRMED:
            _consume_availability(appointment)

        appointment.refresh_from_db()
        return Response(AppointmentReadSerializer(appointment).data)


def _consume_availability(appointment):
    """
    Split any availability slot that overlaps the confirmed 30-minute appointment window.
    Time before and after the appointment is preserved as new slots.
    """
    scheduled_at = appointment.scheduled_at
    slot_date = scheduled_at.date()
    appt_start = scheduled_at.time()
    appt_end = (scheduled_at + timedelta(minutes=30)).time()

    overlapping = ProviderAvailability.objects.filter(
        provider=appointment.provider,
        date=slot_date,
        start_time__lt=appt_end,
        end_time__gt=appt_start,
    )

    for slot in overlapping:
        slot.delete()
        # Preserve time before the appointment
        if slot.start_time < appt_start:
            ProviderAvailability.objects.create(
                provider=appointment.provider,
                date=slot_date,
                start_time=slot.start_time,
                end_time=appt_start,
            )
        # Preserve time after the appointment
        if slot.end_time > appt_end:
            ProviderAvailability.objects.create(
                provider=appointment.provider,
                date=slot_date,
                start_time=appt_end,
                end_time=slot.end_time,
            )
