from django.urls import path

from .views import AgentChatView, AgentSessionView

urlpatterns = [
    path("chat/",    AgentChatView.as_view(),    name="agent-chat"),
    path("session/", AgentSessionView.as_view(), name="agent-session"),
]
