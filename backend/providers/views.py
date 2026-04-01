from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .models import ProviderAvailability, ProviderProfile
from .permissions import IsProvider
from .serializers import ProviderAvailabilitySerializer, ProviderProfileSerializer


class ProviderViewSet(ReadOnlyModelViewSet):
    queryset = ProviderProfile.objects.select_related("user").all()
    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="availability")
    def availability(self, request, pk=None):
        """Return the open availability slots for a given provider."""
        profile = self.get_object()
        slots = (
            ProviderAvailability.objects.filter(provider=profile)
            .order_by("date", "start_time")
        )
        serializer = ProviderAvailabilitySerializer(slots, many=True)
        return Response(serializer.data)


class AvailabilityViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    """Providers manage their own availability slots."""

    queryset = ProviderAvailability.objects.all()
    serializer_class = ProviderAvailabilitySerializer
    permission_classes = [IsProvider]

    def get_queryset(self):
        return (
            ProviderAvailability.objects.filter(provider__user=self.request.user)
            .order_by("date", "start_time")
        )

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user.provider_profile)


class ProviderProfileSelfView(generics.RetrieveUpdateAPIView):
    """Authenticated provider reads or updates their own profile."""

    permission_classes = [IsProvider]
    serializer_class = ProviderProfileSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        profile, _ = ProviderProfile.objects.get_or_create(user=self.request.user)
        return profile
