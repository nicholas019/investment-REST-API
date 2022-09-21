from rest_framework import generics

from api.v1.investments.serializers import  HoldingsListSerializer, TradeInfoSerializer, UserInvestmentDetailSerializer, UserInvestmentSerializer
from apps.investments.models import TradeInfo, UserAssetInfo

from apps.users.models import User


class InvestmentHomeView(generics.ListAPIView):
    '''
    투자화면 API
    토큰을 통해 유저정보를 받아 고객이름, 계좌명, 증권사. 계좌번호, 계좌 총 자산 총 5가지 항목 반환
    '''
    serializer_class = UserInvestmentSerializer

    def get_queryset(self):
        user     = self.request.user
        queryset = User.objects.filter(id = user.id)

        return queryset


class InvestmentDetailView(InvestmentHomeView):
    '''
    투자 상세 화면 API구현
    고객이름, 계좌명, 증권사, 계좌번호, 계좌 총 자산, 투자 원금, 총 수익금, 수익률 8개 데이터 반환
    '''
    serializer_class = UserInvestmentDetailSerializer


class HoldingsView(generics.ListAPIView):    
    '''
    보유종목 화면 API 구현
    고객이름, 보유 종목명, 보유 종목의 자산그룹, 보유 종목의 평가 금액, 보유 종목 ISIN 5개 데이터 반환

    '''
    serializer_class = HoldingsListSerializer

    def get_queryset(self):
        user     = self.request.user
        queryset = UserAssetInfo.objects.filter(user_id = user.id)
        return queryset


class CreateTradeInfo(generics.CreateAPIView):
    '''
    입금거래 정보 저장 API
    정상적으로 입금시 id 반환
    '''
    queryset         = TradeInfo.objects.all()
    serializer_class = TradeInfoSerializer
    