from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from ...models import PasswordReset


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password1"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password1"]:
            raise serializers.ValidationError({"error": "passwords dont match"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError({"error": "passwords dont match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().validate(attrs)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = PasswordReset
        fields = ["email"]


class ResetPasswordSerializer(serializers.Serializer):
    model = User

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password1"]:
            raise serializers.ValidationError({"error": "passwords dont match"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().validate(attrs)
