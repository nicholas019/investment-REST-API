from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from apps.users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["is_active"]

    def validate_password(self, value):
        return make_password(value)