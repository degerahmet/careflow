from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["member", "provider", "scheduled_at", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["member__email", "provider__user__email"]
