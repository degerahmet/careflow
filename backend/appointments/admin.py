from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "member_email", "provider_email", "provider_specialty",
        "scheduled_at", "status", "reason_preview", "created_at",
    )
    search_fields = ("member__email", "provider__user__email", "reason")
    list_filter = ("status", "provider__specialty", "scheduled_at")
    readonly_fields = ("created_at", "updated_at", "ai_summary")
    ordering = ("-scheduled_at",)
    fieldsets = (
        ("Parties", {"fields": ("member", "provider")}),
        ("Details", {"fields": ("scheduled_at", "reason", "status")}),
        ("AI", {"fields": ("ai_summary",), "classes": ("collapse",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Member")
    def member_email(self, obj):
        return obj.member.email

    @admin.display(description="Provider")
    def provider_email(self, obj):
        return obj.provider.user.email

    @admin.display(description="Specialty")
    def provider_specialty(self, obj):
        return obj.provider.get_specialty_display()

    @admin.display(description="Reason")
    def reason_preview(self, obj):
        if len(obj.reason) > 60:
            return obj.reason[:60] + "…"
        return obj.reason
