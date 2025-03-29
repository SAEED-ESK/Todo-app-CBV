from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

urlpatterns = [
    path(
        "registration/", views.RegisterApiView.as_view(), name="registration"
    ),
    # /users/me/
    # path('profile/', views.ProfileApiView.as_view(), name='profile'),
    # /users/resend_activation/
    path("email_test", views.EmailBackend.as_view(), name="email-test"),
    # /users/set_password/
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    # /users/reset_password/
    path(
        "reset_password/",
        views.RequestPasswordReset.as_view(),
        name="reset-password",
    ),
    # /users/reset_password_confirm/
    path(
        "reset_password_confirm/<str:token>/",
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-change",
    ),
    # /users/set_username/
    # /users/reset_username/
    # /users/reset_username_confirm/
    # /token/login/
    path("token/login/", views.CustomAuthToken.as_view(), name="token-login"),
    # /token/logout/
    path(
        "token/logout/", views.LogoutAuthToken.as_view(), name="token-logout"
    ),
    # /jwt/create/
    path(
        "jwt/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    # /jwt/refresh/
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # /jwt/verify/
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
