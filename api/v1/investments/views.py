from rest_framework import generics

from api.v1.investments.serializers import  UserInvestmentSerializer

from apps.users.models import User


class InvestmentHomeView(generics.ListAPIView):
    '''
    투자화면 API
    토큰을 통해 유저정보를 받아 유저이름, 계좌명, 증권사. 계좌번호, 계좌 총 자산 총 5가지 항목 반환
    '''
    serializer_class = UserInvestmentSerializer

    def get_queryset(self):
        user     = self.request.user
        queryset = User.objects.filter(id = user.id)

        return queryset