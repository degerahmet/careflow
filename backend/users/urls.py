from django.urls import path

from users.views import (
    MemberLoginView,
    MemberRegisterView,
    MeView,
    ProviderLoginView,
    ProviderRegisterView,
)

urlpatterns = [
    path("member/register/", MemberRegisterView.as_view(), name="member-register"),
    path("member/login/", MemberLoginView.as_view(), name="member-login"),
    path("provider/register/", ProviderRegisterView.as_view(), name="provider-register"),
    path("provider/login/", ProviderLoginView.as_view(), name="provider-login"),
    path("me/", MeView.as_view(), name="auth-me"),
]
