from django.contrib import admin

from .models import ProviderProfile


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "specialty", "created_at"]
    search_fields = ["user__email", "specialty"]
