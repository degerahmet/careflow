import uuid

from django.conf import settings
from django.db import models


class BookingSession(models.Model):
    STEPS = [
        ("collecting_intent",  "Collecting Intent"),
        ("provider_selection", "Provider Selection"),
        ("slot_selection",     "Slot Selection"),
        ("confirmation",       "Confirmation"),
        ("completed",          "Completed"),
    ]

    session_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    member     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="booking_sessions",
    )
    step  = models.CharField(max_length=32, choices=STEPS, default="collecting_intent")
    draft = models.JSONField(default=dict)
    # draft shape:
    # {
    #   "specialty": "DERMA",
    #   "reason": "rash on arm",
    #   "preferred_date": "2026-04-05",
    #   "selected_provider_id": 3,
    #   "selected_slot_id": 12,
    #   "providers": [...],   # last search_providers result
    #   "slots": [...],       # last get_available_slots result
    # }
    messages   = models.JSONField(default=list)
    # shape: [{"role": "user"|"assistant", "text": "..."}]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BookingSession({self.member.email}, step={self.step})"
