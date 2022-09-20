from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from apps.users.models import AccountInfo, User



class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountInfo
        fields = "__all__"


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["is_active"]

    def validate_password(self, value):
        return make_password(value)
