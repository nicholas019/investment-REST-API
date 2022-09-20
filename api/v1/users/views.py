from rest_framework import generics

from api.v1.users.serializers import UserSignUpSerializer
from apps.users.models import User


class SignUpView(generics.CreateAPIView):
    '''
    본인인증 기능 구현을 위한 계정생성 기능 추가
    uid : 고객아이디, password : 암호, username : 고객명
    '''
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer


