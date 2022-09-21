from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from apps.users.models import User



class UserSignUpSerializer(serializers.ModelSerializer):
    '''
    회원가입용 시리얼라이저
    '''
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["is_active"]

    def validate_password(self, value):
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):
    '''
    조회용 시리얼라이저
    '''
    class Meta:
        model = User
        fields = ["id",'username']