import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class ProviderProfile(models.Model):
    SPECIALTY_CHOICES = [
        ("GEN", "General Practice"),
        ("CARD", "Cardiology"),
        ("DERMA", "Dermatology"),
        ("ENDO", "Endocrinology"),
        ("GAST", "Gastroenterology"),
        ("NEUR", "Neurology"),
        ("PED", "Pediatrics"),
        ("PSY", "Psychiatry"),
        ("RAD", "Radiology"),
        ("SURG", "Surgery"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile",
    )
    specialty = models.CharField(max_length=5, choices=SPECIALTY_CHOICES, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.specialty}"
    
class ProviderAvailability(models.Model):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="availabilities",
    )
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("provider", "date", "start_time", "end_time")

    def __str__(self):
        return f"{self.provider.user.email} — {self.date} {self.start_time}-{self.end_time}"
    
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)