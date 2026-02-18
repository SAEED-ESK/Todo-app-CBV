from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from mail_templated import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ...models import PasswordReset
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer,
)
from ..utils import ThreadEmail


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"username": serializer.validated_data["username"]}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class LogoutAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailBackend(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        email_obj = EmailMessage(
            "email/hello.tpl",
            {"name": "ali"},
            "admin@admin.com",
            to=["kia@gmail.com"],
        )
        ThreadEmail(email_obj).start()
        return Response("mail sent successfully")


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        email = request.data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            reset = PasswordReset(email=email, token=token)
            reset.save()

            # Sending reset link via email (commented out for clarity)
            # ... (email sending code)
            email_obj = EmailMessage(
                "email/reset_password.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            ThreadEmail(email_obj).start()

            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "User with credentials not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if user:
            user.set_password(serializer.data["new_password"])
            user.save()

            reset_obj.delete()

            return Response({"success": "Password updated"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "No user found"}, status=status.HTTP_404_NOT_FOUND
            )
