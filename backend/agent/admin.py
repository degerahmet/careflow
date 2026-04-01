import json

from django.contrib import admin
from django.utils.html import format_html

from .models import BookingSession


@admin.register(BookingSession)
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ("session_id", "member_email", "step", "created_at", "updated_at")
    search_fields = ("session_id", "member__email")
    list_filter = ("step",)
    readonly_fields = (
        "session_id", "member", "step",
        "draft_pretty", "messages_pretty",
        "created_at", "updated_at",
    )
    ordering = ("-updated_at",)
    fields = (
        "session_id", "member", "step",
        "draft_pretty", "messages_pretty",
        "created_at", "updated_at",
    )

    def has_add_permission(self, request):
        return False

    @admin.display(description="Member")
    def member_email(self, obj):
        return obj.member.email

    @admin.display(description="Draft")
    def draft_pretty(self, obj):
        return format_html(
            '<pre style="background:var(--darkened-bg);color:var(--body-fg);'
            'border:1px solid var(--border-color);padding:10px;border-radius:4px;'
            'font-size:12px;line-height:1.5;max-height:300px;overflow:auto;">'
            '{}</pre>',
            json.dumps(obj.draft, indent=2, ensure_ascii=False),
        )

    @admin.display(description="Messages")
    def messages_pretty(self, obj):
        lines = []
        for msg in obj.messages:
            role = msg.get("role", "?")
            text = msg.get("text", "")
            role_color = "var(--primary)" if role == "user" else "var(--body-quiet-color)"
            lines.append(
                f'<div style="margin-bottom:8px;">'
                f'<span style="font-weight:bold;color:{role_color};text-transform:uppercase;'
                f'font-size:11px;">{role}</span><br>'
                f'<span style="white-space:pre-wrap;color:var(--body-fg);">{text}</span>'
                f'</div>'
            )
        if not lines:
            return format_html('<em style="color:var(--body-quiet-color);">No messages yet.</em>')
        return format_html(
            '<div style="background:var(--darkened-bg);color:var(--body-fg);'
            'border:1px solid var(--border-color);padding:10px;border-radius:4px;'
            'font-size:13px;line-height:1.6;max-height:400px;overflow:auto;">'
            '{}</div>',
            format_html("".join(lines)),
        )
