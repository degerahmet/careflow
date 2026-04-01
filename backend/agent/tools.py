import datetime

from django.utils import timezone

from appointments.models import Appointment
from providers.models import ProviderAvailability, ProviderProfile


def search_providers(specialty: str) -> list[dict]:
    """Return providers that match the given specialty code."""
    profiles = ProviderProfile.objects.filter(specialty=specialty).select_related("user")
    return [
        {
            "id": p.id,
            "first_name": p.user.first_name,
            "last_name": p.user.last_name,
            "specialty": p.specialty,
            "bio": p.bio,
        }
        for p in profiles
    ]


def get_available_slots(provider_id: int, preferred_date: str | None = None) -> list[dict]:
    """Return upcoming availability slots for a provider, optionally filtered by date."""
    today = datetime.date.today()
    qs = ProviderAvailability.objects.filter(
        provider_id=provider_id,
        date__gte=today,
    ).order_by("date", "start_time")

    if preferred_date:
        try:
            target = datetime.date.fromisoformat(preferred_date)
            qs = qs.filter(date=target)
        except ValueError:
            pass  # bad date string — return all upcoming slots

    return [
        {
            "id": slot.id,
            "date": slot.date.isoformat(),
            "start_time": slot.start_time.strftime("%H:%M"),
            "end_time": slot.end_time.strftime("%H:%M"),
        }
        for slot in qs[:20]
    ]


def create_appointment(member, provider_id: int, slot_id: int, reason: str) -> dict:
    """Create a pending appointment from a confirmed availability slot."""
    slot = ProviderAvailability.objects.select_related("provider__user").get(id=slot_id)
    scheduled_at = timezone.make_aware(
        datetime.datetime.combine(slot.date, slot.start_time)
    )

    appt = Appointment.objects.create(
        member=member,
        provider=slot.provider,
        scheduled_at=scheduled_at,
        reason=reason,
        ai_summary=reason,
    )
    return {
        "id": appt.id,
        "scheduled_at": appt.scheduled_at.isoformat(),
        "provider_name": f"Dr. {slot.provider.user.first_name} {slot.provider.user.last_name}",
        "status": appt.status,
    }
