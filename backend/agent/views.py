from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from rest_framework.views import APIView

from providers.permissions import IsMember

from .models import BookingSession
from .orchestrator import handle_message
from .serializers import ChatRequestSerializer, ChatResponseSerializer


class AgentSessionView(APIView):
    permission_classes = [IsMember]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="session_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The booking session UUID to retrieve.",
            )
        ],
        responses=ChatResponseSerializer,
    )
    def get(self, request):
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response({"detail": "session_id required."}, status=400)

        session = BookingSession.objects.filter(
            session_id=session_id,
            member=request.user,
        ).first()

        if session is None:
            return Response({"detail": "Session not found."}, status=404)

        draft = session.draft
        return Response({
            "session_id": str(session.session_id),
            "step":       session.step,
            "messages":   session.messages,
            "data": {
                "providers":   draft.get("providers", []),
                "slots":       draft.get("slots", []),
                "appointment": draft.get("appointment"),
                "draft":       {k: v for k, v in draft.items() if k not in ("providers", "slots", "appointment")},
            },
        })


class AgentChatView(APIView):
    permission_classes = [IsMember]

    @extend_schema(request=ChatRequestSerializer, responses=ChatResponseSerializer)
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data.get("session_id")
        message    = serializer.validated_data["message"]

        # Load existing session or create a new one
        session = None
        if session_id:
            session = BookingSession.objects.filter(
                session_id=session_id,
                member=request.user,
            ).first()

        if session is None:
            session = BookingSession.objects.create(member=request.user)

        result = handle_message(session, message)
        return Response(result)
