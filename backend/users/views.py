from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    AuthResponseSerializer,
    MemberLoginSerializer,
    MemberRegisterSerializer,
    ProviderLoginSerializer,
    ProviderRegisterSerializer,
    UserSerializer,
)


def _tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class MemberRegisterView(APIView):
    permission_classes = []

    @extend_schema(
        tags=["Auth - Member"],
        request=MemberRegisterSerializer,
        responses={201: AuthResponseSerializer},
        summary="Register a new member",
    )
    def post(self, request):
        serializer = MemberRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {**UserSerializer(user).data, **_tokens_for_user(user)},
            status=status.HTTP_201_CREATED,
        )


class MemberLoginView(APIView):
    permission_classes = []

    @extend_schema(
        tags=["Auth - Member"],
        request=MemberLoginSerializer,
        responses={200: AuthResponseSerializer},
        summary="Log in as a member",
    )
    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {**UserSerializer(user).data, **_tokens_for_user(user)},
            status=status.HTTP_200_OK,
        )


class ProviderRegisterView(APIView):
    permission_classes = []

    @extend_schema(
        tags=["Auth - Provider"],
        request=ProviderRegisterSerializer,
        responses={201: AuthResponseSerializer},
        summary="Register a new provider",
    )
    def post(self, request):
        serializer = ProviderRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {**UserSerializer(user).data, **_tokens_for_user(user)},
            status=status.HTTP_201_CREATED,
        )


class ProviderLoginView(APIView):
    permission_classes = []

    @extend_schema(
        tags=["Auth - Provider"],
        request=ProviderLoginSerializer,
        responses={200: AuthResponseSerializer},
        summary="Log in as a provider",
    )
    def post(self, request):
        serializer = ProviderLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {**UserSerializer(user).data, **_tokens_for_user(user)},
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Auth"],
        responses={200: UserSerializer},
        summary="Get current user",
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)
