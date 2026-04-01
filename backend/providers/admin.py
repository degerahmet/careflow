from django.contrib import admin

from .models import ProviderAvailability, ProviderProfile


class ProviderAvailabilityInline(admin.TabularInline):
    model = ProviderAvailability
    extra = 0
    fields = ("date", "start_time", "end_time", "created_at")
    readonly_fields = ("created_at",)


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("provider_email", "provider_name", "specialty", "bio_preview", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name", "specialty")
    list_filter = ("specialty",)
    readonly_fields = ("created_at",)
    inlines = [ProviderAvailabilityInline]

    @admin.display(description="Email")
    def provider_email(self, obj):
        return obj.user.email

    @admin.display(description="Name")
    def provider_name(self, obj):
        name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return name or obj.user.email

    @admin.display(description="Bio")
    def bio_preview(self, obj):
        if len(obj.bio) > 80:
            return obj.bio[:80] + "…"
        return obj.bio
